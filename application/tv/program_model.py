# -*- coding: utf-8 -*-
__author__ = 'nikita'


class ProgramModel:
    def __init__(self, channel_id, channel_name, channel_icon,
                 program_name, program_description, time_from, time_to, category):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_icon = channel_icon
        self.program_name = program_name
        self.description = program_description
        self.time_from = time_from
        self.time_to = time_to
        self.category = category


class TVGuideProgram:
    def __init__(self):
        self.programs_vector = []

    def make_channel_vector(self):
        channels_vector = []
        if self.programs_vector:
            for program in self.programs_vector:
                if channels_vector.count(program.channel_id) == 0:
                    channels_vector.append(program.channel_name)
        return channels_vector

    def make_real_program_list(self, going_now):
        if self.programs_vector:
            return [going_now(program) for program in self.programs_vector]
