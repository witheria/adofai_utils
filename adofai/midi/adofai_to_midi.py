from mido import MidiFile, MidiTrack, Message, second2tick, bpm2tempo, MetaMessage
import pretty_midi


# Function to map tile angles to MIDI note pitches
def angle_to_midi_note_angle(angle):
    return 72
    # Normalize angle to 0-360 range
    angle.angle %= 360
    # Map angles to MIDI notes (assuming a range from 60 (C4) to 72 (C5))
    note = 60 + int(angle.angle / 360 * 12)
    return note


# Function to convert tiles to a MIDI file using pretty_midi
def tiles_to_midi_pretty(tiles, output_file: str):
    # Create a PrettyMIDI object
    midi = pretty_midi.PrettyMIDI(initial_tempo=tiles[0].bpm)

    # Create an Instrument instance for a piano instrument
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)

    for tile in tiles:
        print("New Tile: Distance from start>{}".format(tile.distance_from_start))
        note_number = angle_to_midi_note_angle(tile.relative_angle)
        start_time = tile.distance_from_start/1000
        end_time = start_time + (tile.duration / 1000)
        note = pretty_midi.Note(
            velocity=100,
            pitch=note_number,
            start=start_time,
            end=end_time
        )
        piano.notes.append(note)

    # Add the piano instrument to the PrettyMIDI object
    midi.instruments.append(piano)

    # Write out the MIDI data
    midi.write(output_file)


# Function to convert tiles to a MIDI file with mido
def tiles_to_midi(tiles, output_file):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo based on the first tile's BPM (assuming all tiles have the same BPM)
    bpm = tiles[0].bpm
    tempo = bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    # Track the time in ticks
    current_time = 0

    for tile in tiles:

        note = angle_to_midi_note_angle(tile.angle)
        duration_in_ticks = int(second2tick(tile.duration / 1000, mid.ticks_per_beat, tempo))

        # Add note on message
        track.append(Message('note_on', note=note, velocity=64, time=current_time))
        # Add note off message
        track.append(Message('note_off', note=note, velocity=64, time=duration_in_ticks))

        # Update current time
        current_time = 0

    # Save the MIDI file
    mid.save(output_file)

"""
        speed_change = [
            t for t in tile.actions if t.event_type == "SetSpeed"]
        if speed_change:
            if speed_change[0].speedType == "Bpm":
                bpm = speed_change[0].beatsPerMinute
            elif speed_change[0].speedType == "Multiplier":
                bpm *= speed_change[0].bpmMultiplier
            tempo = bpm2tempo(bpm)
            track.append(MetaMessage('set_tempo', tempo=tempo))
"""