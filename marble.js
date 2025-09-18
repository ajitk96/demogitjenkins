// vuln/vuln_strong.js
const http = require('http');
const url = require('url');
const child_process = require('child_process');
const fs = require('fs');
const crypto = require('crypto');

// Hardcoded secret (will be flagged)
const API_KEY = "sk_test_SUPER_SECRET_1234567890";

// Very small unsafe HTTP server to expose many sink points
http.createServer(function (req, res) {
  const q = url.parse(req.url, true).query;

  // 1) Command injection via exec with user control
  if (q.cmd) {
    // intentionally vulnerable: direct user string passed to exec
    child_process.exec(q.cmd, (err, stdout, stderr) => {
      if (err) {
        res.writeHead(500); res.end("err: " + err.toString()); return;
      }
      res.end("cmd out: " + stdout);
    });
    return;
  }

  // 2) Eval usage (RCE-like)
  if (q.eval) {
    try {
      // Dangerous: eval on user-supplied content
      const result = eval(q.eval);
      res.end("eval: " + String(result));
    } catch (e) {
      res.writeHead(500); res.end("eval error");
    }
    return;
  }

  // 3) Path traversal / arbitrary file read
  if (q.file) {
    // no validation → can read /etc/passwd etc.
    fs.readFile(q.file, 'utf8', (err, data) => {
      if (err) res.end("file error: " + err.message);
      else res.end("file data: " + data.slice(0, 1000));
    });
    return;
  }

  // 4) Path traversal / arbitrary file write
  if (q.save && q.name) {
    // no sanitization of name → path traversal
    fs.writeFile('/tmp/uploads/' + q.name, q.save, (err) => {
      if (err) res.end("write error");
      else res.end("saved " + q.name);
    });
    return;
  }

  // 5) Weak crypto usage
  if (q.hash) {
    // MD5 used (weak) — scanners flag weak crypto usage
    const h = crypto.createHash('md5').update(q.hash).digest('hex');
    res.end("md5: " + h);
    return;
  }

  // 6) XSS-like unsafe HTML response
  if (q.name) {
    // directly concatenated into HTML doc
    res.setHeader('Content-Type', 'text/html');
    res.end(`<h1>Hello ${q.name}</h1>`);
    return;
  }

  // default
  res.end("vuln server");
}).listen(8080);

console.log("Vulnerable server (JS) running on http://0.0.0.0:8080");
