function changePassword(csrf_token) {
        var password = [];
        var request = {};
        swal.setDefaults({
          input: 'password',
          confirmButtonText: 'Далее &rarr;',
          showCancelButton: true,
          animation: true,
          progressSteps: ['1', '2']
        });

        var steps = [
          {
            title: 'Изменение пароля',
            text: 'Введите новый пароль'
          },
          'Введите еще раз новый пароль'
        ];

        swal.queue(steps).then(function (result) {
            if(result[0]!==result[1]){
                changePassword(csrf_token);
            }
            else {
                request['ChangePassword'] = 'True';
                request['Password'] = result;
                swal.resetDefaults();
                $.ajax({
                    beforeSend: function (jqXHR) {
                        jqXHR.setRequestHeader("x-csrftoken", csrf_token);
                    },
                    url: window.location.href,
                    data: JSON.stringify(request),
                    type: 'POST',
                    contentType: 'application/json',
                    success: function (data) {
                        if (data['status'] === 'ok') {
                            swal(
                              'Отлично!',
                              'Ваш пароль изменен.',
                              'success'
                            )
                        }
                        if (data['status'] === 'error') {
                            swal(
                                'Упс!',
                                'Изменение пароля было отменено.',
                                'error'
                            )
                        }
                    },
                    error: function (data) {
                        console.log(data.body);
                    }
                });
            }

        }, function () {
            swal.resetDefaults()
        });
    }