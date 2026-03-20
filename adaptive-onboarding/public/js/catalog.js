const searchInput = document.getElementById('catalog-search');
const rows = document.querySelectorAll('.catalog-row');
const countEl = document.getElementById('result-count');

if (searchInput) {
  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase().trim();
    let visible = 0;
    
    rows.forEach(row => {
      // We grab all text including hidden skills explicitly bridged by EJS template
      const text = row.textContent.toLowerCase();
      const match = !query || text.includes(query);
      
      row.style.display = match ? '' : 'none';
      if (match) visible++;
    });
    
    if (countEl) countEl.textContent = visible;
  });
}
