const apiBase = '/api';

async function fetchItems() {
  const response = await fetch(`${apiBase}/items`);
  return response.json();
}

async function addItem(name) {
  const response = await fetch(`${apiBase}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
  return response.json();
}

async function deleteItem(id) {
  await fetch(`${apiBase}/items/${id}`, { method: 'DELETE' });
}

function renderItems(items) {
  const list = document.querySelector('#items-list');
  list.innerHTML = '';

  items.forEach((item) => {
    const listItem = document.createElement('li');
    listItem.textContent = item.name;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.style.marginLeft = '8px';
    deleteButton.addEventListener('click', async () => {
      await deleteItem(item._id);
      await loadItems();
    });

    listItem.appendChild(deleteButton);
    list.appendChild(listItem);
  });
}

async function loadItems() {
  const items = await fetchItems();
  renderItems(items);
}

document.querySelector('#item-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const input = document.querySelector('#item-name');
  const name = input.value.trim();
  if (!name) return;

  await addItem(name);
  input.value = '';
  await loadItems();
});

loadItems().catch((error) => {
  console.error('Failed to load items:', error);
});
