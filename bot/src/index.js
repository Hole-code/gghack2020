require('dotenv').config()


const {Telegraf, session, Scenes: {Stage}} = require('telegraf')
const TSL = require('telegraf-session-local')

const startCommand = require('./commands/start')
const statsCommand = require('./commands/stats')

const distributionScene = require('./scenes/distribution')
//console.log(process.env)



const simulateAsyncPause = () =>
  new Promise(resolve => {
    setInterval(() => resolve(), 1000);
  });


const init = async (bot) => {
    try {
        const stage = new Stage([
            distributionScene, 
        ]);
        bot.use(new TSL({database: 'src/data/session.json'}).middleware())
        bot.use(stage.middleware())
        
        //await users.findOneAndUpdate({photo:{$exists:true}}, {$set:{description:'Переполненна мусорка на улице Красноармейская 7 '}})
        //console.log(lastTask)
        bot.start(startCommand(bot))
        bot.command('stats',statsCommand(bot))
        
        
        //bot.command('task', (ctx)=>{sendTask(ctx,bot,lastTask.photos,lastTask.description,lastTask.date,lastTask.time,lastTask.adress,lastTask.url)})
        
    } catch (error) {
        console.error(error)
    }
    return bot

}

init(new Telegraf(process.env.BOT_TOKEN, {
    polling: true
})).then(async (bot) => {
    await bot.launch();
    console.log("Bot launched", new Date)
})