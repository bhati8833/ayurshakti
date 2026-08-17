import io

robots = open("../robots.txt", encoding="utf-8").read()
# Escape for JS template literal
esc = robots.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
tpl = open("worker.js", encoding="utf-8").read()
tpl = tpl.replace("{{ROBOTS_CONTENT}}", esc)
open("worker.js", "w", encoding="utf-8").write(tpl)
print("Injected", len(robots), "chars into worker.js")
