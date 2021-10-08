window.onload = function (){
    $('.prod_in_basket').on('click','button[type="button"]', function (){
            let t_href = event.target;
            console.log(t_href.name)

            $.ajax({
                url: '/baskets/add/' + t_href.name + '/',
                success: function (data){
                    $('.prod_in_basket').html(data.result)
                },
            });
            event.preventDefault()
        });
}