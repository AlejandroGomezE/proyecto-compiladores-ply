<script>
  import Loading from './Loading.svelte';
  import Message from './Message.svelte';

  export let loading;
  export let error;
  export let compiled_data;
  let execution_actions = [];

  $: if (compiled_data) {
    vm(compiled_data);
  } else {
    execution_actions = [];
  }

  //Unique id of action to render
  let action_id = 0;

  //Scopes refs execution trail
  let scope_ref_stack = [];

  //Execution State management
  let execution_state = {};

  //Current Scope Ref in State Management
  let current_scope_ref = -1;

  //Scopes counter
  let scopes_counter = 0;

  //Return quad
  let return_quad_pointer = [];

  function vm(compiled_data) {
    console.log(compiled_data);

    scopes_counter = 0;

    action_id = 0;

    execution_actions = [];

    scope_ref_stack = [];

    return_quad_pointer = [];

    current_scope_ref = -1;

    execution_state = {
      path_stack: [],
      scopes: {},
    };

    let i = 0;
    while (i < compiled_data.code_quads.length) {
      let quad = compiled_data.code_quads[i];
      let left_operand;
      let right_operand;
      let assign_value;
      let condition;
      let value;

      switch (quad.op_code) {
        case 'start':
          //Add global scope to execution stack
          scope_ref_stack.push(scopes_counter);
          //Add global scope
          add_scope_to_execution_state(current_scope_ref);
          //Add contants to global scope
          Object.keys(compiled_data.constants_table).forEach((key) => {
            let value;
            if (compiled_data.constants_table[key]['type'] === 'string') {
              value = key.replace(/"/g, '');
            } else if (compiled_data.constants_table[key]['type'] === 'float') {
              value = parseFloat(key);
            } else if (compiled_data.constants_table[key]['type'] === 'bool') {
              value = key === 'True' ? true : false;
            }
            set_value_to_address(compiled_data.constants_table[key]['addr'], value);
          });
          i++;
          break;
        case 'main':
          //Add main scope to execution stack
          scope_ref_stack.push(scopes_counter);
          //Add main scope
          add_scope_to_execution_state(current_scope_ref);
          i++;
          break;
        case '+':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand + right_operand);
          i++;
          break;
        case '-':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand - right_operand);
          i++;
          break;
        case '*':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand * right_operand);
          i++;
          break;
        case '/':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand / right_operand);
          i++;
          break;
        case '=':
          assign_value = get_value_from_address(quad.left);
          set_value_to_address(quad.target, assign_value);
          i++;
          break;
        case '<':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand < right_operand);
          i++;
          break;
        case '>':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand > right_operand);
          i++;
          break;
        case '<=':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand <= right_operand);
          i++;
          break;
        case '>=':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand >= right_operand);
          i++;
          break;
        case '==':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand === right_operand);
          i++;
          break;
        case '!=':
          left_operand = get_value_from_address(quad.left);
          right_operand = get_value_from_address(quad.right);
          set_value_to_address(quad.target, left_operand !== right_operand);
          i++;
          break;
        case 'gotoF':
          condition = get_value_from_address(quad.left);
          if (!condition) {
            i = quad.target;
          } else {
            i++;
          }
          break;
        case 'goto':
          i = quad.target;
          break;
        case 'era':
          scope_ref_stack.push(scopes_counter);
          if (scope_ref_stack.at(-1) == scope_ref_stack.at(-2)) {
            add_scope_execution_layer();
          } else {
            add_scope_to_execution_state(current_scope_ref);
          }
          i++;
          break;
        case 'param':
          value = get_value_from_address(quad.left);
          set_value_to_address(quad.target, value);
          i++;
          break;
        case 'gosub':
          return_quad_pointer.push(i + 1);
          i = quad.target;
          break;
        case 'return':
          value = get_value_from_address(quad.left);
          // Add return value to current_scope.scope_layers.at(-2) if scope_ref_stack.at(-2) is equal
          if (scope_ref_stack.at(-1) == scope_ref_stack.at(-2)) {
            set_value_previous_layer(quad.target, value);
          } else {
            // If its returning value to main, set value in global scope layer
            set_value_global(quad.target, value);
          }
          i++;
          break;
        case 'endFunc':
          if (scope_ref_stack.at(-1) == scope_ref_stack.at(-2)) {
            // Popped scope execution layer
            /* console.log(execution_state.scopes[current_scope_ref][scope_layers]).at(-1); */
            pop_scope_execution_layer();
          } else {
            // Popped function scope execution memory
            /* console.log(execution_state.scopes[current_scope_ref]); */
            delete_scope_from_execution_state();
          }
          i = return_quad_pointer.pop();
          break;
        case 'absolute':
          value = get_value_from_address(quad.target);
          add_p_element_to_output_area(Math.abs(value));
          i++;
          break;
        case 'print':
          value = get_value_from_address(quad.target);
          add_p_element_to_output_area(value);
          i++;
          break;
        case 'end':
          console.log(execution_state);
          i++;
          break;
        default:
          i++;
          break;
      }
    }
  }

  // Add scope to execution state
  function add_scope_to_execution_state(parent_ref) {
    execution_state.scopes[scopes_counter] = {
      parent_ref,
      scope_layers: [{}],
    };
    current_scope_ref = scopes_counter;
    execution_state.path_stack.push(scopes_counter);
    scopes_counter++;
  }

  // Pop scope execution layer
  function pop_scope_execution_layer() {
    let current_scope = execution_state.scopes[current_scope_ref];
    current_scope.scope_layers.pop();
    execution_state.path_stack.pop();
    current_scope_ref = execution_state.path_stack[execution_state.path_stack.length - 1];
  }

  //Add scope execution layer
  function add_scope_execution_layer() {
    execution_state.scopes[current_scope_ref].scope_layers.push({});
    execution_state.path_stack.push(current_scope_ref);
  }

  // Delete scope from execution state
  function delete_scope_from_execution_state() {
    let parent_ref = execution_state.scopes[current_scope_ref].parent_ref;
    delete execution_state.scopes[current_scope_ref];
    current_scope_ref = parent_ref;
    execution_state.path_stack.pop();
  }

  // For each scope from current to parent -> parent etc. check their last scope_layer for var address
  function get_scope_ref_from_address(address) {
    // Current scope of execution
    let aux_ref = current_scope_ref;
    while (aux_ref !== -1) {
      let scope = execution_state.scopes[aux_ref];
      // If address has a defines value return scope_ref
      if (scope.scope_layers.at(-1)[address] !== undefined) {
        return aux_ref;
      }
      // Go to parent scope while > -1
      aux_ref = scope.parent_ref;
    }
    return -1;
  }

  // Set value to address
  function set_value_to_address(address, value) {
    // Get scope ref where address is defined
    let aux_ref = get_scope_ref_from_address(address);
    if (aux_ref !== -1) {
      // Modify current value because it exists
      execution_state.scopes[aux_ref].scope_layers.at(-1)[address] = value;
    } else {
      // Create new {address: value} pair in scope layer of current scope
      execution_state.scopes[current_scope_ref].scope_layers.at(-1)[address] = value;
    }
  }

  // Set value to global function address
  function set_value_global(address, value) {
    execution_state.scopes[0].scope_layers.at(-1)[address] = value;
  }

  // Set value to previous scope layer in same scope
  function set_value_previous_layer(address, value) {
    console.log(execution_state.scopes[current_scope_ref].scope_layers.at(-1));
    console.log(execution_state.scopes[current_scope_ref].scope_layers.at(-2));
    execution_state.scopes[current_scope_ref].scope_layers.at(-2)[address] = value;
  }

  // Get value from address
  function get_value_from_address(address) {
    // Get scope ref where address is defined
    let aux_ref = get_scope_ref_from_address(address);
    if (aux_ref !== -1) {
      // Return value for given address
      return execution_state.scopes[aux_ref].scope_layers.at(-1)[address];
    }
  }

  // Get address of functions params
  function get_address_of_function_param(function_name, param_name) {
    let aux_ref = current_scope_ref;
    while (aux_ref !== -1) {
      let scope = compiled_data.scopes_table[aux_ref];

      // Go to parent scope while > -1
      aux_ref = scope.parent_ref;
    }
    return -1;
  }

  // Add p element to output area
  function add_p_element_to_output_area(text) {
    execution_actions.push({
      id: action_id,
      component: Message,
      message: text,
    });
    action_id++;
  }
</script>

<div>
  <label for="output" class="block text-sm font-medium"> Output </label>
  <div class="bg-gray-50 h-[70vh] mt-1 rounded-md overflow-y-auto relative" name="output">
    {#if error}
      <Message message={error} />
    {/if}
    {#if loading}
      <Loading />
    {/if}
    {#each execution_actions as action (action.id)}
      <svelte:component this={action.component} message={action.message} />
    {/each}
  </div>
</div>
