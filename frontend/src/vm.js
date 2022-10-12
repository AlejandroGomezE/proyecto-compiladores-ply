let output_area = document.getElementsByClassName('Output-area');

//Scopes refs execution trail
let scope_ref_stack = [];

//Execution State management
let execution_state = {};

//Current Scope Ref in State Management
let current_scope_ref = -1;

export function vm(compiled_data) {
  scope_ref_stack = [];

  current_scope_ref = -1;

  execution_state = {
    path_stack: [],
    scopes: {},
    scopes_counter: 0,
  };

  output_area[0].innerHTML = '';
  let i = 0;
  while (i < compiled_data.code_quads.length) {
    let quad = compiled_data.code_quads[i];
    let left_operand;
    let right_operand;
    let assign_value;
    let condition;

    switch (quad.op_code) {
      case 'start':
        //Add global scope to execution stack
        scope_ref_stack.push(execution_state.scopes_counter);
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
        scope_ref_stack.push(execution_state.scopes_counter);
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
      case 'print':
        const value = get_value_from_address(quad.target);
        const paragraphElement = document.createElement('p');
        paragraphElement.innerText = '>> ' + value;
        output_area[0].appendChild(paragraphElement);
        i++;
        break;
      case 'end':
        console.log(execution_state);
        i++;
        break;
      default:
        break;
    }
  }
}

// Add scope to execution state
function add_scope_to_execution_state(parent_ref) {
  let current_scope_counter = execution_state.scopes_counter;
  execution_state.scopes[current_scope_counter] = {
    parent_ref,
    scope_layers: [{}],
  };
  current_scope_ref = current_scope_counter;
  execution_state.path_stack.push(current_scope_counter);
  execution_state.scopes_counter++;
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

// Get value from address
function get_value_from_address(address) {
  // Get scope ref where address is defined
  let aux_ref = get_scope_ref_from_address(address);
  if (aux_ref !== -1) {
    // Return value for given address
    return execution_state.scopes[aux_ref].scope_layers.at(-1)[address];
  }
}
