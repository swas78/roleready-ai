const express = require('express');
const router = express.Router();
const multer = require('multer');

// Memory storage up to 5MB
const storage = multer.memoryStorage();
const upload = multer({ storage: storage, limits: { fileSize: 5 * 1024 * 1024 } });

router.get('/', (req, res) => {
    res.render('analyze', { 
        title: 'New Analysis',
        page: 'analyze',
        error: req.query.error || null
    });
});

router.post('/', upload.fields([{ name: 'resume' }, { name: 'jdFile' }]), (req, res) => {
    try {
        let resumeText = req.body.resumeText || "";
        let jdText = req.body.jdText || "";
        const domain = req.body.domain || "tech";
        const demoKey = req.body.demo || null;

        if (req.files) {
            if (req.files.resume && req.files.resume[0]) {
                // Simplified text extraction (PDFs are handled on python side via /analyze/upload if we used that,
                // but prompt says node should extract text from buffer OR use req.body.resumeText.
                // Assuming uploaded file is text/pdf but we just pass the strings for the prompt spec!)
                resumeText = req.files.resume[0].buffer.toString('utf-8');
            }
            if (req.files.jdFile && req.files.jdFile[0]) {
                jdText = req.files.jdFile[0].buffer.toString('utf-8');
            }
        }

        if (!demoKey) {
            if (resumeText.length < 30 || jdText.length < 20) {
                return res.redirect('/analyze?error=Text+too+short.+Please+provide+valid+Resume+and+JD.');
            }
        }

        req.session.resumeText = resumeText;
        req.session.jdText = jdText;
        req.session.domain = domain;
        req.session.demoKey = demoKey;
        req.session.result = null;

        res.redirect('/analyzing');
    } catch (err) {
        console.error("Upload error:", err);
        return res.redirect('/analyze?error=Server+Error+Processing+Upload');
    }
});

module.exports = router;
