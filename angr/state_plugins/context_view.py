
import logging

from .plugin import SimStatePlugin

l = logging.getLogger('angr.state_plugins.context_view')


class ContextView(SimStatePlugin):
    def __init__(self):
        super(ContextView, self).__init__()

    @SimStatePlugin.memo
    def copy(self, memo):
        return ContextView()

    def pprint(self):
        """Pretty context view similiar to the context view of gdb plugins (peda and pwndbg)"""
        raise NotImplementedError

    def registers(self):
        """
        Visualise the register state
        state.arch.default_symbolic_registers is supposed to give a sensible definition of general purpose registers
        Ordering is decided by the VEX register number
        """
        for reg in self.default_registers():
            register_number = self.state.arch.registers[reg][0]
            self.__pprint_register(reg, self.state.registers.load(register_number))

    def __pprint_register(self, reg, value):
        print reg.upper() + ":\t"+ str(value)

    def default_registers(self):
        custom ={
            'X86': ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp', 'eip'],
            'AMD64': ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rbp', 'rsp', 'rip', 'r8', 'r9', 'r10', 'r11', 'r12',
                      'r13', 'r14', 'r15']
        }
        if self.state.arch.name in custom:
            return custom[self.state.arch.name]
        else:
            l.warn("No custom register list implemented, using fallback")
            return self.state.arch.default_symbolic_registers\
                   + [self.state.arch.register_names[self.state.arch.ip_offset]]\
                   + [self.state.arch.register_names[self.state.arch.sp_offset]]\
                   + [self.state.arch.register_names[self.state.arch.bp_offset]]
