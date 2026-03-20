const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    if (!req.session.result) {
        return res.redirect('/analyze');
    }
    res.render('results', { page: 'results', result: req.session.result });
});

// Since the server.js routing has /skills mapped elsewhere, we merge the /skills logic into the root Results.
// The prompt indicated GET /skills on frontend/routes/results.js, which implies this controller serves both!
router.get('/skills', (req, res) => {
    if (!req.session.result) {
        return res.redirect('/analyze');
    }
    res.render('skills', { page: 'skills', result: req.session.result });
});

module.exports = router;
