const API_URL = "http://127.0.0.1:8000/expenses";

const form = document.querySelector(".myForm");
const amount = document.querySelector("#amount");
const category = document.querySelector("#category");
const description = document.querySelector("#description");
const tbody = document.querySelector("tbody");

// --- build one <tr> for one expense object coming from the backend ---
function renderRow(expense) {
  const row = document.createElement("tr");
  row.dataset.id = expense.id; // what is row.da    

  row.innerHTML = `
    <td>${expense.category}</td>
    <td>${expense.description}</td>
    <td>${expense.amount}</td>
    <td><button class="delbtn">Delete</button></td>
  `;

  row.querySelector(".delbtn").addEventListener("click", async () => {
    await deleteExpense(expense.id);
    row.remove();
  });

  tbody.appendChild(row);
}

// --- GET: ask the kitchen "what's already cooking" and paint the table ---
async function loadExpenses() {
  const res = await fetch(API_URL);
  const expenses = await res.json();
  expenses.forEach(renderRow);
}

// --- POST: hand the kitchen a new order slip ---
async function addExpense(newExpense) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newExpense),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail?.[0]?.msg || "Something went wrong");
  }

  return res.json();
}

// --- DELETE: cancel an order by its id ---
async function deleteExpense(id) {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const amountValue = Number(amount.value);
  if (amountValue <= 0 || !amount.value) {
    alert("Amount must be greater than 0");
    return;
  }

  try {
    const saved = await addExpense({
      category: category.value,
      description: description.value,
      amount: amountValue,
    });

    renderRow(saved);

    amount.value = "";
    description.value = "";
  } catch (err) {
    alert(err.message);
  }
});

// on page load, pull whatever the backend already has in memory
loadExpenses();
