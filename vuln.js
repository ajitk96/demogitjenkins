const http = require('http');
const url = require('url');
const child_process = require('child_process');
const fs = require('fs');

// Hardcoded secret
const API_KEY = "sk_live_1234567890abcdef";

// Insecure HTTP server with command injection
http.createServer(function (req, res) {
  const query = url.parse(req.url, true).query;

  // Command injection
  if (query.cmd) {
    child_process.exec(query.cmd, (err, stdout, stderr) => {
      if (err) {
        res.end("Error: " + err.toString());
      } else {
        res.end("Output: " + stdout);
      }
    });
  }

  // Directory traversal / Path injection
  if (query.file) {
    fs.readFile(query.file, 'utf8', (err, data) => {
      if (err) {
        res.end("File error: " + err.toString());
      } else {
        res.end("File content: " + data);
      }
    });
  }

  // XSS vulnerability
  if (query.name) {
    res.end("<h1>Hello " + query.name + "</h1>");
  }

}).listen(8080);

console.log("Vulnerable server running on http://localhost:8080/");
