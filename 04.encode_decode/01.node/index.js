const message = 'Hello, World!';

const encoded = btoa(message);
const decode = atob(encoded);

console.log(encoded); 
console.log(decode);
