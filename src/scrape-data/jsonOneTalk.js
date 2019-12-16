console.log('Starting general conference scraper');
// this program is designed to run on the page
// https://www.churchofjesuschrist.org/study/general-conference/2019/10/11holland?lang=eng
// or similar 

let titleEle = $x("//h1[@id='title1']");
let title = titleEle[0].textContent;

let authorEle = $$(".author-name");
let author = authorEle[0].textContent; 

let paragraphsEles = $x("//div[@class='body-block']//p");
let allText = '';
let paragraphs = [];
for(let i = 0; i < paragraphsEles.length; i++) {
    paragraphs.push(paragraphsEles[i].textContent);
}

let result = {
    title: title,
    author: author,
    paragraphs: paragraphs
}

console.log(result); 

let csvContent = 'data:text/json;charset=ut \n';
csvContent += JSON.stringify(result);

let downloadMe = document.createElement('a'); 
let blob = new Blob(
  [csvContent],{type: 'text/csv;charset=utf-8;'});
let url = URL.createObjectURL(blob);
downloadMe.href = url; 
downloadMe.setAttribute('download', `${title}.csv`); 
downloadMe.click(); 

