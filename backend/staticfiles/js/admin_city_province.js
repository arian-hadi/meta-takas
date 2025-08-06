document.addEventListener('DOMContentLoaded', function () {
  const citySelect = document.getElementById('id_city');
  const provinceSelect = document.getElementById('id_province');

  if (!citySelect || !provinceSelect) return;

  const provinceMap = window.PROVINCE_MAP || {};

  function updateProvinceOptions(selectedCity) {
    provinceSelect.innerHTML = '';

    const provinces = provinceMap[selectedCity] || [];
    if (provinces.length === 0) {
      const option = document.createElement('option');
      option.value = '';
      option.textContent = 'Select a city first';
      provinceSelect.appendChild(option);
    } else {
      provinces.forEach(function (prov) {
        const option = document.createElement('option');
        option.value = prov;
        option.textContent = prov;
        provinceSelect.appendChild(option);
      });
    }
  }

  citySelect.addEventListener('change', function () {
    const selectedCity = citySelect.value;
    updateProvinceOptions(selectedCity);
  });

  // Optional: preload province options if city is already selected
  if (citySelect.value) {
    updateProvinceOptions(citySelect.value);
  }
});
