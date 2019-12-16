console.log('Starting general conference scraper');
// this program is designed to run on the page
// https://www.churchofjesuschrist.org/study/general-conference/2019/10/11holland?lang=eng
// or similar 

let titleEle = $x("//h1[@id='title1']");
let title = titleEle[0].textContent;
// console.log('title', title);

let authorEle = $$(".author-name");
let author = authorEle[0].textContent; 
// console.log('author', author);

let paragraphs = $x("//div[@class='body-block']//p");
let allText = '';
for(let i = 0; i < paragraphs.length; i++) {
    allText += paragraphs[i].textContent + '\n';
}
// console.log('allText', allText);

let csvContent = 'data:text/csv;charset=ut \n';
csvContent += 'title, author, text \n';
csvContent += `${title}, ${author}, ${allText}`;

console.log(csvContent); 

let downloadMe = document.createElement('a'); 
let blob = new Blob(
  [csvContent],{type: 'text/csv;charset=utf-8;'});
let url = URL.createObjectURL(blob);
downloadMe.href = url; 
downloadMe.setAttribute('download', `${title}.csv`); 
downloadMe.click(); 

