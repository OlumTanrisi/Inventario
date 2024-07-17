document.addEventListener("DOMContentLoaded", function() {
    const addProductForm = document.getElementById("add-product-form");
    const updateProductForm = document.getElementById("update-product-form");
    const searchProductForm = document.getElementById("search-product-form");
    const removeProductForm = document.getElementById("remove-product-form");
    const listProductsButton = document.getElementById("list-products");

    addProductForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(addProductForm);
        const data = Object.fromEntries(formData.entries());
        fetch("/add_product", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Error:", error));
    });

    updateProductForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(updateProductForm);
        const data = Object.fromEntries(formData.entries());
        fetch("/update_product", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Error:", error));
    });

    searchProductForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const id = document.getElementById("search-id").value;
        fetch(`/search_product?id=${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById("search-result").textContent = data.message;
            } else {
                document.getElementById("search-result").textContent = JSON.stringify(data);
            }
        })
        .catch(error => console.error("Error:", error));
    });

    removeProductForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const id = document.getElementById("remove-id").value;
        fetch("/remove_product", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Error:", error));
    });

    listProductsButton.addEventListener("click", function() {
        fetch("/list_products")
        .then(response => response.json())
        .then(data => {
            const productsList = document.getElementById("products-list");
            productsList.innerHTML = "";
            data.forEach(product => {
                const productItem = document.createElement("div");
                productItem.textContent = JSON.stringify(product);
                productsList.appendChild(productItem);
            });
        })
        .catch(error => console.error("Error:", error));
    });
});
