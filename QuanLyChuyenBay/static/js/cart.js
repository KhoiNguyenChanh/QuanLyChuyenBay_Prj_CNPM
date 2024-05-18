function addToCart(id, idchuyenbay, price){
    fetch("/api/cart",{
        method: "post",
        body: JSON.stringify({
            "id": id,
            "chuyen_bay_id" : idchuyenbay,
            "price" : price
        }),
        headers: {
            "Content-Type" : "application/json"
        }
    }).then((res) => res.json()).then((data) =>{
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0;i < d.length; i++)
            d[i].innerText = data.total_quantity

    })
}

function updateCart(lich_chuyen_bay_id, obj){
    fetch(`/api/cart/${lich_chuyen_bay_id}`,{
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type" : "application/json"
        }
    }).then((res) => res.json()).then((data) =>{
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0;i < d.length; i++)
            d[i].innerText = data.total_quantity

        let e = document.getElementsByClassName('cart-amount')
        for (let i = 0;i < e.length; i++)
            e[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.error(err))
}

function deleteCart(lcbID) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
         fetch(`/api/cart/${lcbID}`, {
            method: "delete"
        }).then((res) => res.json()).then((data) => {
            console.info(data)
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let a = document.getElementsByClassName('cart-amount')
            for (let i = 0; i < a.length; i++)
                a[i].innerText = data.total_amount.toLocaleString("en-US")

            let e = document.getElementById(`cart${lcbID}`)
            e.style.display = "none"
        }).catch(err => console.error(err))
    }
}

function pay(){
    if(confirm("Bạn chắc muốn thanh toán?") == true){
        fetch("/api/pay").then(res => res.json()).then(data => {
            if(data.status ===200)
                location.reload()
        })
    }
}
function HangVe2(tien,total){
    let tongtien = document.getElementsByClassName("Tongtien").value
//    for (let i = 0;i < tongtien.length; i++)
//            d[i].innerText =tien
////    tongtien.value = tongtien.value + 3*tien
////    tongtien.innerText = tongtien.value
    console.info(tongtien)
}
function HangVe1(tien,total){
    let tongtien = document.getElementById("Tongtien")
    tongtien.innerText = total
    console.info(total)
}

