import fs from 'fs';
import products from './data/products.json'

let prod_list:any = []
for (const [_cat, prods] of Object.entries(products)) {
  for(let prod of prods){
    prod_list.push(prod)
  }
}

function saveFile(name: string, list: any) {
  const json = JSON.stringify(list, null, 2);
  fs.writeFileSync(name, json);
}

function getRandomInt(min: number, max: number) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

function getRandomItems(list: any, n: number) {
  if (n >= list.length) {
    return list;
  }

  let randomItems = [];
  let copyList = list.slice(); 

  for (var i = 0; i < n; i++) {
    let randomIndex = Math.floor(Math.random() * copyList.length);
    let item = copyList[randomIndex];
    randomItems.push(item);
    copyList.splice(randomIndex, 1); 
  }
  return randomItems;
}


// generar detall de ventas
let sells:any = {}

for(let i = 1; i <= 1000; i++){
  let qty = getRandomInt(1, 8)
  let items = getRandomItems(prod_list, qty)

  sells[`${i}`] = []

  for(let item of items){
    let qty2 = getRandomInt(1, 4)

    let obj = {
      "prod": item.nombre,
      "price": item.precio,
      "qty": qty2
    }
    sells[`${i}`].push(obj)
  }
}

saveFile("sell_details.json",sells)
