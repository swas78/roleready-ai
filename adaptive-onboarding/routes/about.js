const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.render('about', {
    title: 'About — RoleReady AI',
    page: 'about'
  });
});

module.exports = router;
