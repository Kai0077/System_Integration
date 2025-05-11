import fs from 'fs';

// const response = await fetch ("https://www.proshop.dk/Computer")
// const result = await response.text();

// fs.writeFileSync("index.html", result);


import {load} from 'cheerio';

const page = await fs.readFileSync("index.html", "utf-8");

console.log(page)

const $ = load(page);

$("#products [product] ").each((index, element) => {
  const name = $(element).find(".site-product-ling").text();
  const price = $(element).find(".site-currency-lg").text();

  console.log("######", name, price);


})