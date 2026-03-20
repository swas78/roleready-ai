require('dotenv').config();
const express = require('express');
const expressLayouts = require('express-ejs-layouts');
const session = require('express-session');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(expressLayouts);
app.set('layout', 'layout');

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(session({
    secret: process.env.SESSION_SECRET || 'fallback-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 3600000, secure: false } // 1 hour
}));

if (process.env.NODE_ENV === 'development') {
    app.use((req, res, next) => {
        console.log(`[DEBUG] ${req.method} ${req.path}`, Object.keys(req.session));
        next();
    });
}

// Routes
app.use('/', require('./routes/index'));
app.use('/about', require('./routes/about'));
app.use('/catalog', require('./routes/catalog'));
app.use('/demo', require('./routes/demo'));
app.use('/analyze', require('./routes/analyze'));
app.use('/analyzing', require('./routes/analyzing'));
app.use('/results', require('./routes/results'));
app.use('/skills', require('./routes/skills'));

app.use((req, res) => {
    res.status(404).render('404', { page: '404' });
});

app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('<h1>500 Internal Server Error</h1><p>Check console for details.</p>');
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on port ${port}`));
