const express = require('express');
const router = express.Router();
const { getCatalog } = require('../api/backend');

router.get('/', async (req, res) => {
  try {
    const data = await getCatalog();
    res.render('catalog', {
      title: 'Course Catalog — RoleReady AI',
      page: 'catalog',
      courses: data.courses || [],
      total: data.total || 0
    });
  } catch (err) {
    res.render('catalog', {
      title: 'Course Catalog — RoleReady AI',
      page: 'catalog',
      courses: [],
      total: 0
    });
  }
});

module.exports = router;
