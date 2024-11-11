# Auto Drozer

**Auto Drozer** is a tool designed to automate the usage of [Drozer](https://labs.f-secure.com/tools/drozer/) using a `commands.yml` file to define the 
commands to be run. It returns a html file that can be viewed on a browser and also a json file.

## Usage

```bash
Usage: python main.py <commands.yml> <output.json> <package_name>
```
Example

```bash
python main.py ../commands.yml results.json io.hextree.attacksurface1
    ___         __           ____                            
   /   | __  __/ /_____     / __ \_________  ____  ___  _____
  / /| |/ / / / __/ __ \   / / / / ___/ __ \/_  / / _ \/ ___/
 / ___ / /_/ / /_/ /_/ /  / /_/ / /  / /_/ / / /_/  __/ /    
/_/  |_\__,_/\__/\____/  /_____/_/   \____/ /___/\___/_/     
                                                             

[ + ] [INFO] Executing: Package Information
[ + ] [INFO] Running command: run app.package.info -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Attack Surface Analysis
[ + ] [INFO] Running command: run app.package.attacksurface io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Package Backup
[ + ] [INFO] Running command: run app.package.backup -f io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Activity Information
[ + ] [INFO] Running command: run app.activity.info -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Detailed Activity Information with Intent and URI
[ + ] [INFO] Running command: run app.activity.info -i -u -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Broadcast Information with Intent and URI
[ + ] [INFO] Running command: run app.broadcast.info -i -u -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Native Library Information
[ + ] [INFO] Running command: run app.package.native io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Content Provider Information with URI Access
[ + ] [INFO] Running command: run app.provider.info -u -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Find Content Provider URIs
[ + ] [INFO] Running command: run app.provider.finduri io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Service Information with Intent and URI
[ + ] [INFO] Running command: run app.service.info -i -u -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Native Code Scanner
[ + ] [INFO] Running command: run scanner.misc.native -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Readable Files in Data Directory
[ + ] [INFO] Running command: run scanner.misc.readablefiles /data/data/io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Duplicate Readable Files Check in Data Directory
[ + ] [INFO] Running command: run scanner.misc.readablefiles /data/data/io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Find URIs for Accessible Content Providers
[ + ] [INFO] Running command: run scanner.provider.finduris -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: SQL Tables in Content Providers
[ + ] [INFO] Running command: run scanner.provider.sqltables -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ + ] [INFO] Executing: Directory Traversal in Content Providers
[ + ] [INFO] Running command: run scanner.provider.traversal -a io.hextree.attacksurface1
[ ✔ ] [SUCCESS] Command executed successfully.
[ ✔ ] [SUCCESS] Results saved to results.json
[ ✔ ] [SUCCESS] HTML file created: results.html
```

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/auto-drozer.git
cd auto-drozer
```

Install the requirements

```bash
pip install -r requirements.txt
```


## Custom rules

You can define your own custom commands to run in `commands.yml`. Just add a title and a drozer commands as follows

```yml
- title: "Package Information"
  command: "run app.package.info -a {package}"
- title: "Custom title"
  command: "Custom command"
```
