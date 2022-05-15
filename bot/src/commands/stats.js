







const fs = require('fs')
module.exports = (bot) => async (ctx)=>{
    const {
        MongoClient
    } = require('mongodb')
    const client = new MongoClient('mongodb://45.10.42.122:27017/')
    await client.connect()
    const db = client.db('tasks')
    const stats2 = db.collection('stats2')
    const photo = await stats2.findOne({})
    const photoBase = photo['photo']
    //console.log(photoBase)
    const statsPhoto = Buffer.from(photoBase.toString(),'base64')
    //fs.writeFileSync('../src/data/stats.jpg',statsPhoto)
    //const photoFromFile = fs.readFileSync('../src/data/stats.jpg')
    ctx.tg.sendPhoto(ctx.chat.id,{source:statsPhoto},{reply_markup:{inline_keyboard:[[{text:'Вернутся в режим просмотра',callback_data:'delete'}]]}})
    bot.action(/.+$/,(ctx)=>{
        let userAction = ctx.match[0]
        switch(userAction){
            case 'delete':
                ctx.tg.deleteMessage(ctx.chat.id, ctx.update.callback_query.message.message_id)
        }
    })

    // try {
    // } catch (error) {
    //     ctx.tg.sendPhoto(ctx.chat.id,{source:fs.readFileSync('../src/data/stats.jpg')}) 
    // }

    //return(ctx.scene.enter('distribution'))
}