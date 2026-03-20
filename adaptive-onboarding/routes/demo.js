const express = require('express');
const router = express.Router();
const { loadDemo } = require('../api/backend');

router.get('/', async (req, res) => {
  try {
    const [senior, fresher, ops] = await Promise.all([
      loadDemo('senior'),
      loadDemo('fresher'),
      loadDemo('ops')
    ]);
    res.render('demo', {
      title: 'Demo Profiles — RoleReady AI',
      page: 'demo',
      profiles: { senior, fresher, ops }
    });
  } catch (err) {
    console.error('Demo page error:', err);
    res.status(500).send('Demo data unavailable — is uvicorn running?');
  }
});

// Keeping the JSON load endpoint intact for the UI smoke test triggers organically
router.get('/load/:profile', async (req, res) => {
    try {
        const { profile } = req.params;
        const data = await loadDemo(profile);
        res.json(data);
    } catch (err) {
        res.status(500).json({ error: 'Failed to load demo payload.' });
    }
});

module.exports = router;
