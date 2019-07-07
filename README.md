# universe
Minimal unmanaged file-sharing/blog site

## Installation
```bash
git clone https://github.com/d3npa/universe.git && cd universe
pip install -r requirements.txt
python3 ./app.py
```
The app will run listen on `127.0.0.1:5000` by default.
You can forward to it by using a proxy such as Nginx or Apache.

## Usage
Files placed in the `contents/` folder will be accessible from the web. 
The index file is located at `contents/posts/index.txt` (subject to change).

#### File extensions matter!
- `.md` and `.markdown` will load as a Markdown file
- `.txt` will load as HTML, but with extra functionality such as bash command parsing (see below).
- `.html` and `.htm` will load as regular HTML.
- `.png`, `.jpg`, `.mp3`, `.mp4`, `.pdf` will load as their respective mimetypes.

#### Bash command parsing
Bash commands may be executed in-line as the file is viewed using the `$(echo 'hello world')` syntax inside a `.txt` file. 
**!! Note that these commands are executed whenever a user views the page.**<br>
**!! It is the admin's responsibility to ensure commands run will not result unintended behavior.**
