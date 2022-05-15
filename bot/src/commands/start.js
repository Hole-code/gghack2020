
module.exports = (bot) => async (ctx)=>{
    ctx.tg.sendMessage(ctx.chat.id,'Бот запущен, ожидайте заданий')
    return(ctx.scene.enter('distribution'))
}