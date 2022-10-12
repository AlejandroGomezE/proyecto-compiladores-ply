let output_area = document.getElementById('output-area');

//Scopes refs execution trail
let scope_ref_stack = [];

export function vm(compiled_data) {
  compiled_data.code_quads.forEach(async (quad) => {
    switch (quad.op_code) {
      case 'start':
        scope_ref_stack.push(0);
        break;
      case 'print':
        console.log(quad.target);
        break;
      case 'end':
        break;
      default:
        break;
    }
  });
}
