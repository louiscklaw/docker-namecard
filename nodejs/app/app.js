var app = require('express')();
var http = require('http').Server(app);

// serving
app.get('/', function (req, res) {
    res.sendfile('contacts.json');
});


http.listen(3000, function () {
    console.log('listening on 3000');
});
