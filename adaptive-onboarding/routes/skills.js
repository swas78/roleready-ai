const express = require('express');
const router = express.Router();
const { getCatalog } = require('../api/backend');

router.get('/', async (req, res) => {
  try {
    const catalog = await getCatalog();
    res.render('skills', {
      title: 'Skill Graph — RoleReady AI',
      page: 'skills',
      catalog: catalog
    });
  } catch (err) {
    console.error('Skills page error:', err);
    res.render('skills', {
      title: 'Skill Graph — RoleReady AI',
      page: 'skills',
      catalog: { courses: [], total: 0 }
    });
  }
});

module.exports = router;
