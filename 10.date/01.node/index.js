console.log(new Date()) //UTC

console.log(Date()) //Local Time

console.log(Date.now()) //UTC

const date = new Date();

console.log("##################");
const danishDate = new Intl.DateTimeFormat('da-DK').format(date);
console.log(danishDate);

console.log("##################");
const americanDate = new Intl.DateTimeFormat('en-us').format(date);

console.log(americanDate);