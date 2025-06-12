const formData = new FormData();
formData.append('nombre', 'AirMax97');
formData.append('stock', '35');  // Importante: siempre string, FormData trata todo como string

fetch('http://127.0.0.1:8000/api/productos/update/3/', {
  method: 'PATCH',
  body: formData
})
.then(response => {
  if (!response.ok) throw new Error('Error al actualizar');
  return response.json();
})
.then(data => {
  console.log('✅ Producto actualizado:', data);
})
.catch(err => {
  console.error('❌ Error:', err);
});
