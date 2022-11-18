<script>
  import Loading from './Loading.svelte';
  import Message from './Message.svelte';

  export let loading;
  export let error;
  export let compiled_data;
  let inputDisabled = true;
  let inputValue = '';
  let inputType = 'text';
  let execution_actions = [];

  $: if (compiled_data) {
    vm(compiled_data);
  } else {
    execution_actions = [];
  }

  //Unique id of action to render
  let action_id = 0;

  //Scopes refs execution trail
  let scopes_ref_execution_stack = [];

  //Execution State management
  let execution_state = {};

  //Current Scope Ref in State Management
  let current_scope_ref = -1;

  //Scopes counter
  let scopes_counter = 0;

  //Return quad
  let return_quad_pointer = [];

  const handleInput = (e) => {
    // in here, you can switch on type and implement
    // whatever behaviour you need
    inputValue = inputType.match(/^(number|range)$/) ? +e.target.value : e.target.value;
  };

  function waitListener(element, listenerName) {
    if (!element) return;
    return new Promise(function (resolve, reject) {
      var listener = (event) => {
        element.removeEventListener(listenerName, listener);
        resolve(event);
      };
      element.addEventListener(listenerName, listener);
    });
  }

  async function vm(compiled_data) {
    console.log(compiled_data);

    scopes_counter = 0;

    action_id = 0;

    execution_actions = [];

    scopes_ref_execution_stack = [];

    return_quad_pointer = [];

    current_scope_ref = -1;

    execution_state = {
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
          //Add global scope
          add_scope_to_execution_state(current_scope_ref);
          //Add contants to global scope
          Object.keys(compiled_data.constants_table).forEach((key) => {
            let value;
            if (compiled_data.constants_table[key]['type'] === 'string') {
              value = key.replace(/"/g, '');
            } else if (compiled_data.constants_table[key]['type'] === 'float') {
              value = parseFloat(key);
            } else if (compiled_data.constants_table[key]['type'] === 'int') {
              value = parseInt(key);
            } else if (compiled_data.constants_table[key]['type'] === 'bool') {
              value = key === 'True' ? true : false;
            }
            set_value_to_address(compiled_data.constants_table[key]['addr'], value);
          });
          i++;
          break;
        case 'main':
          //Add main scope
          add_scope_to_execution_state(current_scope_ref);
          i++;
          break;
        case '+':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand + right_operand);
          i++;
          break;
        case '-':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand - right_operand);
          i++;
          break;
        case '*':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand * right_operand);
          i++;
          break;
        case '/':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand / right_operand);
          i++;
          break;
        case '=':
          assign_value = get_value_from_address(quad.left);
          if (compiled_data.virtual_var_list.includes(quad.target)) {
            set_value_to_address(get_value_from_address(quad.target), assign_value);
          } else {
            set_value_to_address(quad.target, assign_value);
          }
          i++;
          break;
        case '<':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand < right_operand);
          i++;
          break;
        case '>':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand > right_operand);
          i++;
          break;
        case '<=':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand <= right_operand);
          i++;
          break;
        case '>=':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand >= right_operand);
          i++;
          break;
        case '==':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
          set_value_to_address(quad.target, left_operand === right_operand);
          i++;
          break;
        case '!=':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            left_operand = get_value_from_address(get_value_from_address(quad.left));
          } else {
            left_operand = get_value_from_address(quad.left);
          }
          if (compiled_data.virtual_var_list.includes(quad.right)) {
            right_operand = get_value_from_address(get_value_from_address(quad.right));
          } else {
            right_operand = get_value_from_address(quad.right);
          }
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
          add_scope_to_execution_state(current_scope_ref);
          i++;
          break;
        case 'param':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            value = get_value_from_address(get_value_from_address(quad.left));
          } else {
            value = get_value_from_address(quad.left);
          }
          set_value_to_address(quad.target, value);
          i++;
          break;
        case 'gosub':
          return_quad_pointer.push(i + 1);
          i = quad.target;
          break;
        case 'return':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            value = get_value_from_address(get_value_from_address(quad.left));
          } else {
            value = get_value_from_address(quad.left);
          }
          set_value_global(quad.target, value);
          delete_scope_from_execution_state();
          i = return_quad_pointer.pop();
          break;
        case 'endFunc':
          delete_scope_from_execution_state();
          i = return_quad_pointer.pop();
          break;
        case 'ver':
          let s1 = get_value_from_address(quad.target);
          if (!Number.isInteger(s1)) {
            add_p_element_to_output_area('Error: Trying to access array with non-integer index');
            i = compiled_data.quad_list.length - 1;
            break;
          }
          let d1 = get_value_from_address(quad.right);
          if (s1 < 0 || s1 > d1) {
            add_p_element_to_output_area('Error: Index out of bounds');
            i = compiled_data.quad_list.length - 1;
            break;
          }
          i++;
          break;
        case '+v':
          let k = get_value_from_address(quad.right);
          set_value_global(quad.target, quad.left + k);
          i++;
          break;
        case 'absolute':
          if (compiled_data.virtual_var_list.includes(quad.left)) {
            value = get_value_from_address(get_value_from_address(quad.left));
          } else {
            value = get_value_from_address(quad.left);
          }
          if (quad.target) {
            set_value_to_address(quad.target, Math.abs(value));
          } else {
            add_p_element_to_output_area(Math.abs(value));
          }
          i++;
          break;
        case 'print':
          if (compiled_data.virtual_var_list.includes(quad.target)) {
            value = get_value_from_address(get_value_from_address(quad.target));
          } else {
            value = get_value_from_address(quad.target);
          }
          if (!value) {
            add_p_element_to_output_area('Error: Trying to print uninitialized value');
            i = compiled_data.code_quads.length - 1;
            loading = false;
            inputDisabled = true;
            inputValue = '';
            break;
          }
          add_p_element_to_output_area(value.toString());
          i++;
          break;
        case 'read':
          inputDisabled = false;
          if (quad.left == 'int' || quad.left == 'float') {
            inputType = 'number';
          } else {
            inputType = 'text';
          }
          loading = true;
          await waitListener(document.getElementById('readValue'), 'click');
          if (inputValue === 'True') {
            inputValue = true;
          } else if (inputValue === 'False') {
            inputValue = false;
          }
          if (typeof inputValue === 'string') {
            if (quad.left != 'string') {
              add_p_element_to_output_area('Error: Trying to read a string into a non-string variable');
              i = compiled_data.code_quads.length - 1;
              loading = false;
              inputDisabled = true;
              inputValue = '';
              break;
            }
            inputValue = inputValue.replace(/"/g, '');
          } else if (typeof inputValue === 'number' && !Number.isInteger(inputValue)) {
            if (quad.left != 'float') {
              add_p_element_to_output_area('Error: Trying to read a float into a non-float variable');
              i = compiled_data.code_quads.length - 1;
              loading = false;
              inputDisabled = true;
              inputValue = '';
              break;
            }
            inputValue = parseFloat(inputValue);
          } else if (typeof inputValue === 'number' && Number.isInteger(inputValue)) {
            if (quad.left != 'int') {
              add_p_element_to_output_area('Error: Trying to read an int into a non-int variable');
              i = compiled_data.code_quads.length - 1;
              loading = false;
              inputDisabled = true;
              inputValue = '';
              break;
            }
            inputValue = parseInt(inputValue);
          } else if (typeof inputValue === 'boolean') {
            if (quad.left != 'bool') {
              add_p_element_to_output_area('Error: Trying to read a bool into a non-bool variable');
              i = compiled_data.code_quadsasd.length - 1;
              loading = false;
              inputDisabled = true;
              inputValue = '';
              break;
            }
            inputValue = inputValue === 'True' ? true : false;
          }
          set_value_to_address(quad.target, inputValue);
          loading = false;
          inputDisabled = true;
          inputValue = '';
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
    scopes_ref_execution_stack.push(scopes_counter);
    execution_state.scopes[scopes_counter] = {
      parent_ref,
      scope_memory: {},
    };
    current_scope_ref = scopes_counter;
    scopes_counter++;
  }

  // Delete scope from execution state
  function delete_scope_from_execution_state() {
    delete execution_state.scopes[current_scope_ref];
    scopes_ref_execution_stack.pop();
    current_scope_ref = scopes_ref_execution_stack.at(-1);
    scopes_counter--;
  }

  // For each scope from current to parent -> parent etc. check their last scope_memory for var address
  function get_scope_ref_from_address(address) {
    // Current scope of execution
    let aux_ref = current_scope_ref;
    while (aux_ref !== -1) {
      let scope = execution_state.scopes[aux_ref];
      // If address has a defines value return scope_ref
      if (scope.scope_memory[address] !== undefined) {
        return aux_ref;
      }
      // Go to parent scope while > -1
      aux_ref = scope.parent_ref;
    }
    return -1;
  }

  // Set value to address
  function set_value_to_address(address, value) {
    if (compiled_data.virtual_var_list.includes(address)) {
      address = get_value_from_address(address);
    }
    // Get scope ref where address is defined
    let aux_ref = get_scope_ref_from_address(address);
    if (aux_ref !== -1) {
      // Modify current value because it exists
      execution_state.scopes[aux_ref].scope_memory[address] = value;
    } else {
      // Create new {address: value} pair in scope layer of current scope
      execution_state.scopes[current_scope_ref].scope_memory[address] = value;
    }
  }

  // Set value to global function address
  function set_value_global(address, value) {
    execution_state.scopes[0].scope_memory[address] = value;
  }

  // Get value from address
  function get_value_from_address(address) {
    let aux_ref = get_scope_ref_from_address(address);
    // Get scope ref where address is defined
    if (aux_ref !== -1) {
      // Return value for given address
      return execution_state.scopes[aux_ref].scope_memory[address];
    }
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

<div class="flex flex-col">
  <label for="output" class="block text-sm font-medium"> Output </label>
  <div class="bg-gray-50 h-[70vh] mt-1 rounded-md overflow-y-auto relative" name="output">
    {#if error}
      <Message message={error} />
    {/if}
    {#if loading}
      <Loading />
    {:else}
      {#each execution_actions as action (action.id)}
        <svelte:component this={action.component} message={action.message} />
      {/each}
    {/if}
  </div>
  <div class="mt-2 flex gap-1">
    <input on:input={handleInput} value={inputValue} disabled={inputDisabled} type={inputType} class="w-3/4" />
    <button
      id="readValue"
      type="button"
      on:click={() => {}}
      disabled={inputDisabled}
      class="w-1/4 rounded-md border border-transparent bg-blue-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
    >
      Read
    </button>
  </div>
</div>
