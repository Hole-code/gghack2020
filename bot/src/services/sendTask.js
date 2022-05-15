const fs = require('fs')
module.exports = async (ctx, bot, photos64, description, date, time, adress, url) => {
    let messageText = `
${description} 
Обращение поступило: ${date} 
в ${time}, 
мусорка по адрессу: ${adress}`
    let photos = []
    //console.log(photos64)
    for (let index = 0; index < 2; index++) {
        //console.log(photos64[index])
        const photo = Buffer.from(photos64[index].toString(), "base64");
        //console.log(photos64[index])
        //if()

        photos.push(photo)
    }
    ctx.telegram.sendPhoto(ctx.chat.id, {
        source: photos[0]
    }, {
        caption: messageText,
        reply_markup: {
            inline_keyboard: [
                [{
                    text: 'Отправить уборщика',
                    callback_data: 'workerSent'
                }],[{
                    text: 'Отправить машину',
                    callback_data: 'carSent'
                }],
                [{
                    text: 'Это ошибка',
                    callback_data: 'mistake'
                }]
            ]
        }
    })
}