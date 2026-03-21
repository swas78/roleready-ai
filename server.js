require('dotenv').config();
const express = require('express');
const expressLayouts = require('express-ejs-layouts');
const session = require('express-session');
const path = require('path');
const csrfProtection = require('csurf');
const cookieParser = require('cookie-parser');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(expressLayouts);
app.set('layout', 'layout');

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

app.use(session({
    secret: process.env.SESSION_SECRET || 'fallback-secret',
    resave: false,
    saveUninitialized: false,
    cookie: {
        maxAge: 3600000, // 1 hour
        secure: process.env.NODE_ENV === 'production', // Only send over HTTPS in production
        httpOnly: true, // Prevent XSS access to session cookie
        sameSite: 'strict' // Prevent CSRF attacks
    }
}));

// CSRF protection middleware
app.use(csrfProtection());

// Middleware to pass CSRF token to all templates
app.use((req, res, next) => {
    res.locals.csrfToken = req.csrfToken();
    next();
});

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

// Error handling middleware
app.use((err, req, res, next) => {
    // Handle CSRF token errors
    if (err.code === 'EBADCSRFTOKEN') {
        res.status(403).render('error', {
            page: 'error',
            message: 'Invalid CSRF token. Please try again.',
            status: 403
        });
    } else {
        console.error(err.stack);
        res.status(500).render('error', {
            page: 'error',
            message: 'Internal Server Error',
            status: 500
        });
    }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on port ${port}`));
