# universe
A minimal unmanaged blog app written in Flask

## Installation
```bash
git clone https://github.com/d3npa/universe.git && cd universe
pip install -r requirements.txt
python3 ./app.py | tee -a access.log
```
The app will run listen on `127.0.0.1:5000` by default.<br>
You can (and should) proxy connections to it via Nginx, Relayd, Apache etc.

## Usage
Files placed in the `contents/` folder will be accessible from the web.
The index file is located at `contents/.index.txt`.
There is also a 404 message defined in `contents/.404.txt`.

#### File extensions matter!
- `.md` and `.markdown` will be parsed by [Markdown](https://pypi.org/project/Markdown/).
- `.txt` will load as HTML, but with extra functionality such as inline bash commands (see below).
- `.html` and `.htm` will load as regular HTML.
- `.png`, `.jpg`, `.mp3`, `.mp4`, `.pdf` will load as their respective mimetypes.

#### Bash command parsing
Bash commands may be executed in-line as the file is viewed using the following syntax:
```html
<h1>$(echo 'Title')</h1> <!-- All in regular HTML -->
<pre><code>$(echo 'Title' | hexdump -C)</code></pre>
```
Which turns into:
```html
<h1>Title</h1> <!-- All in regular HTML -->
<pre><code>00000000  54 69 74 6c 65                                    |Title|
00000005
</code></pre>
```
**!! Note: These commands are executed on the server whenever a user views the page.**<br>
**!! It is the admin's responsibility to ensure commands are safe to execute.**

## Warning
If a [*Local File Inclusion*](https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion) (LFI) vulnerability were to be discovered, an `access_log.txt` file could be exploited to gain arbitrary remote code execution (RCE). Using any other extension, such as `access.log`, mitigates this problem, as only `.txt` files may contain executable bash commands. Consider doing the same with any other file written by the web server.
