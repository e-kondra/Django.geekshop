window.onload = function (){
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
};