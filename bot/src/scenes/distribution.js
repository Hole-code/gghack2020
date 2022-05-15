





const {
    Scenes: {
        BaseScene
    }
} = require('telegraf')
const distribution = new BaseScene('distribution');
const {
    MongoClient
} = require('mongodb')
const client = new MongoClient('mongodb://45.10.42.122:27017/')
const sendTask = require('../services/sendTask')


try {
    distribution.enter(async (ctx) => {
        try {
            await client.connect()
            const tasksDB = client.db('tasks')
            const carsCollection = tasksDB.collection('cars')
            const workersCollection = tasksDB.collection('workers')
            const mistakesCollection = tasksDB.collection('fail')

            const general = client.db('tasks').collection('general')
            //console.log(users)
            const tasks = await general.find({}).sort({
                _id: -1
            }).limit(2).toArray()
            var lastTask = tasks[0]
            // changeStream = client.db('tasks').collection('general').watch()
            // changeStream.on("change", next => {
            //     console.log("received a change to the collection: \t", next);
            // });
            //sendTask(ctx, ctx, lastTask.photos, lastTask.description, lastTask.date, lastTask.time, lastTask.adress, lastTask.url)
            const checkUpdate = async () => {
                let updateTasks = await general.find({}).sort({
                    _id: -1
                }).limit(2).toArray()

                let checkLastTask = updateTasks[0]
                console.log(checkLastTask.time)
                console.log(new Date)
                if (lastTask._id < checkLastTask._id) {
                    console.log('new!')
                    lastTask = checkLastTask
                    sendTask(ctx, ctx, lastTask.photos, lastTask.description, lastTask.date, lastTask.time, lastTask.adress, lastTask.url)
                }
            }
            distribution.action(/.+$/,(ctx)=>{
                let userAction = ctx.match[0]
                switch(userAction){
                    case 'workerSent':
                        workersCollection.findOneAndUpdate({_id:{$exists:true}},{$inc:{count:1}})
                        ctx.tg.deleteMessage(ctx.chat.id, ctx.update.callback_query.message.message_id)
                        break
                    case 'carSent':
                        carsCollection.findOneAndUpdate({_id:{$exists:true}},{$inc:{count:1}})
                        ctx.tg.deleteMessage(ctx.chat.id, ctx.update.callback_query.message.message_id)
                        break
                    case 'mistake':
                        mistakesCollection.findOneAndUpdate({_id:{$exists:true}},{$inc:{count:1}})
                        ctx.tg.deleteMessage(ctx.chat.id, ctx.update.callback_query.message.message_id)
                        break
                }
            })
            setInterval(() => {
                checkUpdate()
            }, 2000)
        } catch (err) {
            console.log(err)
        }
    })
} catch (error) {
    console.log(error)
}


module.exports = distribution