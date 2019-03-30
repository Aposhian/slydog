from evaluate import evaluateSingleSample, prep_net

beam_size, encoder, decoder, voc = prep_net()

print(evaluateSingleSample('hi there', beam_size, encoder, decoder, voc))

print(evaluateSingleSample('you look nice', beam_size, encoder, decoder, voc))

print(evaluateSingleSample('I think you are very crazy', beam_size, encoder, decoder, voc))