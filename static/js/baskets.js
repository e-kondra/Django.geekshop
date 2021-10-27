window.addEventListener("load", function(evt){
    $('.basket_list').on('click','input[type="number"]', function(){ //basket_list-это класс в нашем baskets.html
        let t_href = event.target;
        // console.log(t_href.name);
        // console.log(t_href.value);

        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/', // путь как в urls 'edit/<int:id>/<int:quantity>/' + переменные так же должны называться
            success: function (data){
                $('.basket_list').html(data.result) // здесь возвращается текст-html(baskets.html) с новыми(измененными) данными
            },
        });
        event.preventDefault()
    });

    $('.products_add').on('click','button[type="button"]', (e)=> {
        $(document).on('click', '.products_add', (e) => {
            let t_href = e.target;

            console.log(t_href.name);
            // console.log(t_href.value);
            let csrf = $('meta[name="csrf-token"]').attr('content');
            // let page_id = t_href.value;
            $.ajax({
                type: 'POST',
                headers: {
                    "X-CSRFToken":csrf
                },
                url: '/baskets/add/' + t_href.name + '/', // путь как в urls 'edit/<int:id>/<int:quantity>/' + переменные так же должны называться
                // data: {'page_id': page_id},
                success: function (data) {
                    // if (data) {
                    $('.products_list').html(data.result) // здесь возвращается текст-html с новыми(измененными) данными
                    // }
                },
            });
            e.preventDefault();
        });
    });
});