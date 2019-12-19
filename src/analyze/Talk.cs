namespace analyze {
    class Talk {
    private string title;
    private string author; 
    private string[] paragraphs;

        public Talk(string title, string author, string[] paragraphs) {
            this.title = title;
            this.author = author;
            this.paragraphs = paragraphs;
        }
    }
}