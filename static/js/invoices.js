document.addEventListener('DOMContentLoaded', function() {
    const itemsBody = document.getElementById('itemsBody');
    const btnAddRow = document.getElementById('btnAddRow');
    const shippingInput = document.getElementById('shipping_charge');
    
    // Add first row by default
    if (itemsBody) {
        addRow();
        
        btnAddRow.addEventListener('click', addRow);
        shippingInput.addEventListener('input', calculateTotals);
        
        // Save handlers
        document.getElementById('btnSaveDraft').addEventListener('click', () => saveInvoice('Draft'));
        document.getElementById('btnGenerate').addEventListener('click', () => saveInvoice('Pending'));
    }

    function addRow() {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <input type="text" class="premium-input item-name mb-2" placeholder="Item Name" required>
                <input type="text" class="premium-input item-desc text-small" placeholder="Description (Optional)">
            </td>
            <td><input type="number" class="premium-input item-qty text-right" value="1" min="1" step="1"></td>
            <td><input type="number" class="premium-input item-price text-right" value="0.00" min="0" step="0.01"></td>
            <td><input type="number" class="premium-input item-tax text-right" value="0" min="0" step="0.1"></td>
            <td><input type="number" class="premium-input item-disc text-right" value="0" min="0" step="0.1"></td>
            <td class="text-right"><span class="item-total font-bold">$0.00</span></td>
            <td class="text-center">
                <button class="btn-remove-row text-red bg-transparent" style="border:none;cursor:pointer;" title="Remove">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </td>
        `;
        
        itemsBody.appendChild(tr);
        
        // Add event listeners for this row
        const inputs = tr.querySelectorAll('input');
        inputs.forEach(input => input.addEventListener('input', calculateTotals));
        
        tr.querySelector('.btn-remove-row').addEventListener('click', function() {
            if (itemsBody.children.length > 1) {
                tr.remove();
                calculateTotals();
            } else {
                alert("You must have at least one item.");
            }
        });
    }

    function calculateTotals() {
        let subtotal = 0;
        let totalTax = 0;
        let totalDiscount = 0;

        const rows = itemsBody.querySelectorAll('tr');
        rows.forEach(row => {
            const qty = parseFloat(row.querySelector('.item-qty').value) || 0;
            const price = parseFloat(row.querySelector('.item-price').value) || 0;
            const taxPct = parseFloat(row.querySelector('.item-tax').value) || 0;
            const discPct = parseFloat(row.querySelector('.item-disc').value) || 0;

            const baseLineTotal = qty * price;
            const lineDisc = baseLineTotal * (discPct / 100);
            const lineTotalAfterDisc = baseLineTotal - lineDisc;
            const lineTax = lineTotalAfterDisc * (taxPct / 100);
            
            const lineTotal = lineTotalAfterDisc + lineTax;

            row.querySelector('.item-total').textContent = '$' + lineTotal.toFixed(2);
            row.dataset.lineTotal = lineTotal.toFixed(2);

            subtotal += baseLineTotal;
            totalDiscount += lineDisc;
            totalTax += lineTax;
        });

        const shipping = parseFloat(shippingInput.value) || 0;
        const grandTotal = subtotal - totalDiscount + totalTax + shipping;

        document.getElementById('lblSubtotal').textContent = '$' + subtotal.toFixed(2);
        document.getElementById('lblTotalDiscount').textContent = '-$' + totalDiscount.toFixed(2);
        document.getElementById('lblTotalTax').textContent = '+$' + totalTax.toFixed(2);
        document.getElementById('lblGrandTotal').textContent = '$' + grandTotal.toFixed(2);

        // Store values for submission
        document.getElementById('lblSubtotal').dataset.val = subtotal;
        document.getElementById('lblTotalDiscount').dataset.val = totalDiscount;
        document.getElementById('lblTotalTax').dataset.val = totalTax;
        document.getElementById('lblGrandTotal').dataset.val = grandTotal;
    }

    async function saveInvoice(saveStatus) {
        // Basic Validation
        const customerName = document.getElementById('customer_name').value;
        if (!customerName) {
            alert("Customer Name is required.");
            document.getElementById('customer_name').focus();
            return;
        }

        const btnDraft = document.getElementById('btnSaveDraft');
        const btnGen = document.getElementById('btnGenerate');
        btnDraft.disabled = true;
        btnGen.disabled = true;
        btnGen.innerHTML = 'Saving...';

        const items = [];
        const rows = itemsBody.querySelectorAll('tr');
        rows.forEach(row => {
            const name = row.querySelector('.item-name').value;
            if (name) {
                items.push({
                    product_name: name,
                    description: row.querySelector('.item-desc').value,
                    quantity: row.querySelector('.item-qty').value,
                    unit_price: row.querySelector('.item-price').value,
                    tax_percentage: row.querySelector('.item-tax').value,
                    discount_percentage: row.querySelector('.item-disc').value,
                    line_total: row.dataset.lineTotal
                });
            }
        });

        const payload = {
            customer_name: customerName,
            company_name: document.getElementById('company_name').value,
            phone_number: document.getElementById('phone_number').value,
            email_address: document.getElementById('email_address').value,
            billing_address: document.getElementById('billing_address').value,
            gst_number: document.getElementById('gst_number').value,
            
            invoice_number: document.getElementById('invoice_number').value,
            invoice_date: document.getElementById('invoice_date').value,
            due_date: document.getElementById('due_date').value,
            status: saveStatus, // Draft goes as Pending or Draft if we added Draft. The view defaults to Pending.
            
            subtotal: document.getElementById('lblSubtotal').dataset.val || 0,
            total_discount: document.getElementById('lblTotalDiscount').dataset.val || 0,
            total_tax: document.getElementById('lblTotalTax').dataset.val || 0,
            shipping_charge: document.getElementById('shipping_charge').value || 0,
            grand_total: document.getElementById('lblGrandTotal').dataset.val || 0,
            
            payment_method: document.getElementById('payment_method').value,
            bank_account_details: document.getElementById('bank_account_details').value,
            upi_id: document.getElementById('upi_id').value,
            
            notes: document.getElementById('notes').value,
            terms_conditions: document.getElementById('terms_conditions').value,
            items: items
        };

        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            
            if (data.success) {
                window.location.href = '/finance/invoices/';
            } else {
                alert('Error saving invoice: ' + data.error);
                btnDraft.disabled = false;
                btnGen.disabled = false;
                btnGen.innerHTML = 'Generate Invoice';
            }
        } catch (error) {
            console.error(error);
            alert('A network error occurred.');
            btnDraft.disabled = false;
            btnGen.disabled = false;
            btnGen.innerHTML = 'Generate Invoice';
        }
    }
});
