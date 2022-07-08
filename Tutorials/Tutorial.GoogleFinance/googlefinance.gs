/**
 * To get stock price from google finance
 *
 * @param {number} code - stock code for Tokyo Exchange
 * @return stockprice
 * @customfunction
 */
function TOKYO_STOCK_PRICE(code) {
  let url = 'https://www.google.com/finance/quote/' + code + ':TYO';
  let html = UrlFetchApp.fetch(url).getContentText();
  let stockPrice = Parser.data(html)
    .from('<div class="YMlKec fxKbKc">')
    .to('</div>')
    .build();
  console.log('StockPrice:'+stockPrice);
  return stockPrice;
}
