from system import *

print("Loading...")
progressbar()

clear_screen()
from dialog import *
from entity import *
from func import *
from intent import *
from preprocess import *
from action import *

clear_screen()

#NER
emodel = NER()

#Dialog
MAX_SEQ_LEN_IN = 15
MAX_SEQ_LEN_OUT = 30

dinput_word_model, doutput_word_model, dpairs = \
    prepare_json_data('input', 'output', './dialog.json', MAX_SEQ_LEN_OUT, name = "Dialog")

dinput_seqs = [pair[0] for pair in dpairs]
doutput_seqs = [pair[1] for pair in dpairs]

#print([input_seq for input_seq in dinput_seqs])

dpadded_input = pad_sequences(dinput_seqs, MAX_SEQ_LEN_IN)
dpadded_output = pad_sequences(doutput_seqs, MAX_SEQ_LEN_OUT)

done_hot_input = one_hot_encode(dpadded_input, dinput_word_model, MAX_SEQ_LEN_IN)
done_hot_output = one_hot_encode(dpadded_output, doutput_word_model, MAX_SEQ_LEN_OUT)

done_hot_target = one_hot_encode_target(dpadded_output, doutput_word_model, MAX_SEQ_LEN_OUT)


dmodel = DialogModel(done_hot_input, done_hot_output, done_hot_target)
dmodel.encoder(293)
dmodel.decoder(152)
dmodel.load(name = 'Full')

print("\n")

#Intent

MAX_SEQ_LEN = 25
iinput_word_model, ioutput_word_model, ipairs = \
    prepare_json_data('input', 'output', './intents.json', MAX_SEQ_LEN_IN, name = "Intent")

input_seqs = [pair[0] for pair in ipairs]
intent = [pair[1] for pair in ipairs]

ipadded_input = pad_sequences(input_seqs, MAX_SEQ_LEN_OUT)

ione_hot_input = one_hot_encode(ipadded_input, iinput_word_model, MAX_SEQ_LEN_IN)
ione_hot_output = one_hot_encode([intent], ioutput_word_model, len(intent))[0]


Imodel = IntentModel("onehot")
Imodel = Imodel(ione_hot_input, ione_hot_output, 244, 53)

Imodel.load(name = 'Full')

actionJar = Actions()



emodel.AddCustomReplaceWords(list(set([intent[1] for intent in ipairs if '{'+intent[1]+'}' not in intent[0].split(' ')])), 'skill')

# Adding the Actions to the intents...

# actionJar.Add(INTENT, FUNCTION)

actionJar.Add('ip', get_ip)
actionJar.Add('time', get_time)
actionJar.Add('date', get_date)
actionJar.Add('cpu.max.process', get_cpu_max_process)
actionJar.Add('weather.current', get_weather_current)
actionJar.Add('weather.next.hour', get_weather_current)
actionJar.Add('weather.next.day', get_weather_next_day)
actionJar.Add('why.did.skill.fail', why_skill_failed)
actionJar.Add('alarm.remove', remove_alarm)
actionJar.Add('alarm.list', list_alarm)
actionJar.Add('alarm.set', set_alarm)
actionJar.Add('joke', get_jokes)

# Actions that do needs but do not have an associated function yet
actionJar.Add('say')
actionJar.Add('pair')
actionJar.Add('spell')
actionJar.Add('show')
actionJar.Add('open.path')
actionJar.Add('ask')
actionJar.Add('remove.all')
actionJar.Add('add')
actionJar.Add('open.palce')
actionJar.Add('update.all')
actionJar.Add('remove')
actionJar.Add('update')
actionJar.Add('math')
actionJar.Add('alarm.stop')
actionJar.Add('pandora.play')
actionJar.Add('pandora.next')
actionJar.Add('pandora.end')
actionJar.Add('pandora.stop')
actionJar.Add('cpu.total.usage')
actionJar.Add('cpu.usage.application')
actionJar.Add('mem.free')
actionJar.Add('record.end')
actionJar.Add('mem.usage.application')
actionJar.Add('mem.max.process')
actionJar.Add('record.begin')
actionJar.Add('playback.begin')
actionJar.Add('mem.total')
actionJar.Add('mem.used')
actionJar.Add('how.do.i.activate')



clear_screen()



print("All modules loaded successfully...")
print("Closed domain task oriented bot operational...")
print("\n")

try:
    while True:
        _input = input("You : ")
        ipadded_input = [pad_sequence(_input.lower(), MAX_SEQ_LEN_IN).split()]
        ione_hot = one_hot_encode(ipadded_input, iinput_word_model, MAX_SEQ_LEN_IN)
        intent, iconfidence = Imodel.decode(ione_hot, ioutput_word_model)
        print("\n\t intent: ", intent, iconfidence)
        
        
        _input, entities = emodel.GetAllEntities(_input)
        print('\t entity:', entities)
        


        '''
        print(actionJar.ExecuteAction(intent, entities))
        '''

        _input = ':' + intent + ': ' + _input
        #print('\t', _input)
        
        dpadded_input = [pad_sequence(_input, len(_input.split(' '))).split()]
        done_hot = one_hot_encode(dpadded_input, dinput_word_model, MAX_SEQ_LEN_IN)
        dprediction, dconfidence = dmodel.decode(done_hot, doutput_word_model, MAX_SEQ_LEN_OUT)
        #print("\t\tresponse: ", dprediction, dconfidence)

        print('\t  dialog:', dprediction, dconfidence, '\n')
        
        print("Bot : ", actionJar.GetFeedbackDialog(intent, entities, dprediction))
        
        print('\n')
        
except KeyboardInterrupt:
    pass
