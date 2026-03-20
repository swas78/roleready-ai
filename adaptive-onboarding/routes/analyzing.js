const express = require('express');
const router = express.Router();
const backend = require('../api/backend');

router.get('/', (req, res) => {
    if (!req.session.resumeText && !req.session.demoKey) {
        return res.redirect('/analyze');
    }
    res.render('analyzing', { page: 'analyzing' });
});

router.get('/run', async (req, res) => {
    try {
        let result;
        if (req.session.demoKey) {
            result = await backend.loadDemo(req.session.demoKey);
        } else {
            result = await backend.analyzeProfile({
                resumeText: req.session.resumeText,
                jdText: req.session.jdText,
                domain: req.session.domain
            });
        }

        req.session.result = result;
        
        // Critical: Force session save before sending ok
        req.session.save((err) => {
            if (err) {
                console.error("Session save error:", err);
                return res.status(500).json({ ok: false, error: 'Failed to write session data' });
            }
            res.json({ ok: true });
        });

    } catch (err) {
        console.error("Analyzing Error:", err);
        res.status(500).json({ ok: false, error: err.message });
    }
});

module.exports = router;
