#!/usr/bin/env python

import sys
import os
import random
import re
sys.path += os.path.abspath(os.path.join(os.path.split(__file__)[0], "../pylib")),


def error(msg, ctx):
    from yapps import runtime
    err = runtime.SyntaxError(None, msg, ctx)
    runtime.print_error(err, ctx.scanner)
    sys.exit(1)


class pack:
    def __init__(self, **kv):
        self.__dict__.update(kv)
    def __str__(self):
        return str(self.__dict__)

def std_rename(t):
    if t in ["string", "map", "list", "set", "deque", "vector", "unordered_map", "unordered_set"]:
        t = "std::" + t
    return t

def forbid_reserved_names(name):
    if re.match("__([^_]+.*[^_]+|[^_])__$", name):
        raise Exception("bad name '%s', __NAME__ format names are reserved" % name)


# Begin -- grammar generated by Yapps
import sys, re
from yapps import runtime

class RpcScanner(runtime.Scanner):
    patterns = [
        ('"0"', re.compile('0')),
        ('"="', re.compile('=')),
        ('"\\)"', re.compile('\\)')),
        ('"\\|"', re.compile('\\|')),
        ('"\\("', re.compile('\\(')),
        ('"raw"', re.compile('raw')),
        ('"fast"', re.compile('fast')),
        ('"service"', re.compile('service')),
        ('"abstract"', re.compile('abstract')),
        ('"long"', re.compile('long')),
        ('"unsigned"', re.compile('unsigned')),
        ('"int"', re.compile('int')),
        ('"bool"', re.compile('bool')),
        ('">"', re.compile('>')),
        ('","', re.compile(',')),
        ('"<"', re.compile('<')),
        ('"i64"', re.compile('i64')),
        ('"i32"', re.compile('i32')),
        ('"}"', re.compile('}')),
        ('"{"', re.compile('{')),
        ('"struct"', re.compile('struct')),
        ('"::"', re.compile('::')),
        ('"namespace"', re.compile('namespace')),
        ('\\s+', re.compile('\\s+')),
        ('//[^\\n]+', re.compile('//[^\\n]+')),
        (';', re.compile(';')),
        ('EOF', re.compile('($|%%)')),
        ('SYMBOL', re.compile('[a-zA-Z_][a-zA-Z0-9_]*')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{';':None,'\\s+':None,'//[^\\n]+':None,},str,*args,**kw)

class Rpc(runtime.Parser):
    Context = runtime.Context
    def rpc_source(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'rpc_source', [])
        namespace = None
        if self._peek('"namespace"', 'EOF', '"struct"', '"abstract"', '"service"', context=_context) == '"namespace"':
            namespace_decl = self.namespace_decl(_context)
            namespace = namespace_decl
        structs_and_services = self.structs_and_services(_context)
        EOF = self._scan('EOF', context=_context)
        return pack(namespace=namespace, structs=structs_and_services.structs, services=structs_and_services.services)

    def namespace_decl(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'namespace_decl', [])
        self._scan('"namespace"', context=_context)
        SYMBOL = self._scan('SYMBOL', context=_context)
        namespace = [SYMBOL]
        while self._peek('"::"', 'EOF', '"struct"', '"abstract"', '"service"', context=_context) == '"::"':
            self._scan('"::"', context=_context)
            SYMBOL = self._scan('SYMBOL', context=_context)
            namespace += SYMBOL,
        return namespace

    def structs_and_services(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'structs_and_services', [])
        structs = []; services = []
        while self._peek('"struct"', '"abstract"', '"service"', 'EOF', context=_context) != 'EOF':
            _token = self._peek('"struct"', '"abstract"', '"service"', context=_context)
            if _token == '"struct"':
                struct_decl = self.struct_decl(_context)
                structs += struct_decl,
            else: # in ['"abstract"', '"service"']
                service_decl = self.service_decl(_context)
                services += service_decl,
        return pack(structs=structs, services=services)

    def struct_decl(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'struct_decl', [])
        self._scan('"struct"', context=_context)
        SYMBOL = self._scan('SYMBOL', context=_context)
        self._scan('"{"', context=_context)
        struct_fields = self.struct_fields(_context)
        self._scan('"}"', context=_context)
        return pack(name=SYMBOL, fields=struct_fields)

    def struct_fields(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'struct_fields', [])
        fields = []
        while self._peek('"}"', '"i32"', '"i64"', '"bool"', '"int"', '"unsigned"', '"long"', '"::"', 'SYMBOL', context=_context) != '"}"':
            struct_field = self.struct_field(_context)
            fields += struct_field,
        return fields

    def struct_field(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'struct_field', [])
        type = self.type(_context)
        SYMBOL = self._scan('SYMBOL', context=_context)
        return pack(name=SYMBOL, type=type)

    def type(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'type', [])
        _token = self._peek('"i32"', '"i64"', '"bool"', '"int"', '"unsigned"', '"long"', '"::"', 'SYMBOL', context=_context)
        if _token == '"i32"':
            self._scan('"i32"', context=_context)
            return "rpc::i32"
        elif _token == '"i64"':
            self._scan('"i64"', context=_context)
            return "rpc::i64"
        elif _token in ['"::"', 'SYMBOL']:
            full_symbol = self.full_symbol(_context)
            t = std_rename(full_symbol)
            if self._peek('"<"', 'SYMBOL', '","', '">"', '"\\|"', '"\\)"', context=_context) == '"<"':
                self._scan('"<"', context=_context)
                type = self.type(_context)
                t += "<" + type
                while self._peek('">"', '","', context=_context) == '","':
                    self._scan('","', context=_context)
                    type = self.type(_context)
                    t += ", " + type
                self._scan('">"', context=_context)
                t += ">"
            return t
        else: # in ['"bool"', '"int"', '"unsigned"', '"long"']
            _token = self._peek('"bool"', '"int"', '"unsigned"', '"long"', context=_context)
            if _token == '"bool"':
                self._scan('"bool"', context=_context)
            elif _token == '"int"':
                self._scan('"int"', context=_context)
            elif _token == '"unsigned"':
                self._scan('"unsigned"', context=_context)
            else: # == '"long"'
                self._scan('"long"', context=_context)
            error("please use i32 or i64 for any integer types", _context)

    def full_symbol(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'full_symbol', [])
        s = ""
        if self._peek('"::"', 'SYMBOL', context=_context) == '"::"':
            self._scan('"::"', context=_context)
            s += "::"
        SYMBOL = self._scan('SYMBOL', context=_context)
        s += SYMBOL
        while self._peek('"::"', '"<"', 'SYMBOL', '","', '">"', '"\\|"', '"\\)"', context=_context) == '"::"':
            self._scan('"::"', context=_context)
            SYMBOL = self._scan('SYMBOL', context=_context)
            s += "::" + SYMBOL
        return s

    def service_decl(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'service_decl', [])
        abstract = False
        if self._peek('"abstract"', '"service"', context=_context) == '"abstract"':
            self._scan('"abstract"', context=_context)
            abstract = True
        self._scan('"service"', context=_context)
        SYMBOL = self._scan('SYMBOL', context=_context)
        self._scan('"{"', context=_context)
        service_functions = self.service_functions(_context)
        self._scan('"}"', context=_context)
        return pack(name=SYMBOL, abstract=abstract, functions=service_functions)

    def service_functions(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'service_functions', [])
        functions = []
        while self._peek('"fast"', '"raw"', 'SYMBOL', '"}"', context=_context) != '"}"':
            service_function = self.service_function(_context)
            functions += service_function,
        return functions

    def service_function(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'service_function', [])
        attr = None; abstract = False; input = []; output = []
        if self._peek('"fast"', '"raw"', 'SYMBOL', context=_context) != 'SYMBOL':
            _token = self._peek('"fast"', '"raw"', context=_context)
            if _token == '"fast"':
                self._scan('"fast"', context=_context)
                attr = "fast"
            else: # == '"raw"'
                self._scan('"raw"', context=_context)
                attr = "raw"
        SYMBOL = self._scan('SYMBOL', context=_context)
        forbid_reserved_names(SYMBOL)
        self._scan('"\\("', context=_context)
        func_arg_list = self.func_arg_list(_context)
        input = func_arg_list
        if self._peek('"\\|"', '"\\)"', context=_context) == '"\\|"':
            self._scan('"\\|"', context=_context)
            func_arg_list = self.func_arg_list(_context)
            output = func_arg_list
        self._scan('"\\)"', context=_context)
        if self._peek('"="', '"fast"', '"raw"', 'SYMBOL', '"}"', context=_context) == '"="':
            self._scan('"="', context=_context)
            self._scan('"0"', context=_context)
            abstract = True
        return pack(name=SYMBOL, attr=attr, abstract=abstract, input=input, output=output)

    def func_arg_list(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'func_arg_list', [])
        args = []
        _token = self._peek('"i32"', '"i64"', '"bool"', '"int"', '"unsigned"', '"long"', '","', '"::"', 'SYMBOL', '"\\|"', '"\\)"', context=_context)
        if _token in ['","', '"\\|"', '"\\)"']:
            pass
        else:
            func_arg = self.func_arg(_context)
            args = [func_arg]
            while self._peek('","', '"\\|"', '"\\)"', context=_context) == '","':
                self._scan('","', context=_context)
                func_arg = self.func_arg(_context)
                args += func_arg,
        return args

    def func_arg(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'func_arg', [])
        name = None
        type = self.type(_context)
        if self._peek('SYMBOL', '","', '"\\|"', '"\\)"', context=_context) == 'SYMBOL':
            SYMBOL = self._scan('SYMBOL', context=_context)
            name = SYMBOL; forbid_reserved_names(name)
        return pack(name=name, type=type)


def parse(rule, text):
    P = Rpc(RpcScanner(text))
    return runtime.wrap_error_reporter(P, rule)

# End -- grammar generated by Yapps



class SourceFile(object):
    def __init__(self, f):
        self.f = f
        self.indent_level = 0
    def indent(self):
        class Indent:
            def __init__(self, sf):
                self.sf = sf
            def __enter__(self):
                self.sf.indent_level += 1
            def __exit__(self, type, value, traceback):
                self.sf.indent_level -= 1
        return Indent(self)
    def incr_indent(self):
        self.indent_level += 1
    def decr_indent(self):
        self.indent_level -= 1
        assert self.indent_level >= 0
        
    def write(self, txt):
        self.f.write(txt)
        
    def writeln(self, txt=None):
        if txt != None:
            self.f.write("    " * self.indent_level)
            self.f.write(txt)
        self.f.write("\n")

def emit_struct(struct, f):
    f.writeln("struct %s {" % struct.name)
    with f.indent():
        for field in struct.fields:
            f.writeln("%s %s;" % (field.type, field.name))
    f.writeln("};")
    f.writeln()
    f.writeln("inline rpc::Marshal& operator <<(rpc::Marshal& m, const %s& o) {" % struct.name)
    with f.indent():
        for field in struct.fields:
            f.writeln("m << o.%s;" % field.name)
        f.writeln("return m;")
    f.writeln("}")
    f.writeln()
    f.writeln("inline rpc::Marshal& operator >>(rpc::Marshal& m, %s& o) {" % struct.name)
    with f.indent():
        for field in struct.fields:
            f.writeln("m >> o.%s;" % field.name)
        f.writeln("return m;")
    f.writeln("}")
    f.writeln()


def emit_service_and_proxy(service, f):
    f.writeln("class %sService: public rpc::Service {" % service.name)
    f.writeln("public:")
    with f.indent():
        f.writeln("enum {")
        with f.indent():
            for func in service.functions:
                rpc_code = random.randint(0x10000000, 0x70000000)
                f.writeln("%s = %s," % (func.name.upper(), hex(rpc_code)))
        f.writeln("};")
        f.writeln("int reg_to(rpc::Server* svr) {")
        with f.indent():
            f.writeln("int ret = 0;")
            for func in service.functions:
                if func.attr == "raw":
                    f.writeln("if ((ret = svr->reg(%s, this, &%sService::%s)) != 0) {" % (func.name.upper(), service.name, func.name))
                else:
                    f.writeln("if ((ret = svr->reg(%s, this, &%sService::__%s__wrapper__)) != 0) {" % (func.name.upper(), service.name, func.name))
                with f.indent():
                    f.writeln("goto err;")
                f.writeln("}")
            f.writeln("return 0;")
        f.writeln("err:")
        with f.indent():
            for func in service.functions:
                f.writeln("svr->unreg(%s);" % func.name.upper())
            f.writeln("return ret;")
        f.writeln("}")
        f.writeln("// these RPC handler functions need to be implemented by user")
        f.writeln("// for 'raw' handlers, remember to reply req, delete req, and sconn->release(); use sconn->run_async for heavy job")
        for func in service.functions:
            if service.abstract or func.abstract:
                postfix = " = 0"
            else:
                postfix = ""
            if func.attr == "raw":
                f.writeln("virtual void %s(rpc::Request* req, rpc::ServerConnection* sconn)%s;" % (func.name, postfix))
            else:
                func_args = []
                for in_arg in func.input:
                    if in_arg.name != None:
                        func_args += "const %s& %s" % (in_arg.type, in_arg.name),
                    else:
                        func_args += "const %s&" % in_arg.type,
                for out_arg in func.output:
                    if out_arg.name != None:
                        func_args += "%s* %s" % (out_arg.type, out_arg.name),
                    else:
                        func_args += "%s*" % out_arg.type,
                f.writeln("virtual void %s(%s)%s;" % (func.name, ", ".join(func_args), postfix))
    f.writeln("private:")
    with f.indent():
        for func in service.functions:
            if func.attr == "raw":
                continue
            f.writeln("void __%s__wrapper__(rpc::Request* req, rpc::ServerConnection* sconn) {" % func.name)
            with f.indent():
                if func.attr != "fast":
                    f.writeln("auto f = [=] {")
                    f.incr_indent()
                invoke_with = []
                in_counter = 0
                out_counter = 0
                for in_arg in func.input:
                    f.writeln("%s in_%d;" % (in_arg.type, in_counter))
                    f.writeln("req->m >> in_%d;" % in_counter)
                    invoke_with += "in_%d" % in_counter,
                    in_counter += 1
                for out_arg in func.output:
                    f.writeln("%s out_%d;" % (out_arg.type, out_counter))
                    invoke_with += "&out_%d" % out_counter,
                    out_counter += 1
                f.writeln("this->%s(%s);" % (func.name, ", ".join(invoke_with)))
                f.writeln("sconn->begin_reply(req);")
                for i in range(out_counter):
                    f.writeln("*sconn << out_%d;" % i)
                f.writeln("sconn->end_reply();")
                f.writeln("delete req;")
                f.writeln("sconn->release();")
                if func.attr != "fast":
                    f.decr_indent()
                    f.writeln("};")
                    f.writeln("sconn->run_async(f);")
            f.writeln("}")
    f.writeln("};")
    f.writeln()
    f.writeln("class %sProxy {" % service.name)
    f.writeln("protected:")
    with f.indent():
        f.writeln("rpc::Client* __cl__;")
    f.writeln("public:")
    with f.indent():
        f.writeln("%sProxy(rpc::Client* cl): __cl__(cl) { }" % service.name)
        for func in service.functions:
            async_func_params = []
            async_call_params = []
            sync_func_params = []
            sync_out_params = []
            in_counter = 0
            out_counter = 0
            for in_arg in func.input:
                if in_arg.name != None:
                    async_func_params += "const %s& %s" % (in_arg.type, in_arg.name),
                    async_call_params += in_arg.name,
                    sync_func_params += "const %s& %s" % (in_arg.type, in_arg.name),
                else:
                    async_func_params += "const %s& in_%d" % (in_arg.type, in_counter),
                    async_call_params += "in_%d" % in_counter,
                    sync_func_params += "const %s& in_%d" % (in_arg.type, in_counter),
                in_counter += 1
            for out_arg in func.output:
                if out_arg.name != None:
                    sync_func_params += "%s* %s" % (out_arg.type, out_arg.name),
                    sync_out_params += out_arg.name,
                else:
                    sync_func_params += "%s* out_%d" % (out_arg.type, out_counter),
                    sync_out_params += "out_%d" % out_counter,
                out_counter += 1
            f.writeln("rpc::Future* async_%s(%sconst rpc::FutureAttr& __fu_attr__ = rpc::FutureAttr()) {" % (func.name, ", ".join(async_func_params + [""])))
            with f.indent():
                f.writeln("rpc::Future* __fu__ = __cl__->begin_request(%sService::%s, __fu_attr__);" % (service.name, func.name.upper()))
                if len(async_call_params) > 0:
                    f.writeln("if (__fu__ != nullptr) {")
                    with f.indent():
                        for param in async_call_params:
                            f.writeln("*__cl__ << %s;" % param)
                    f.writeln("}")
                f.writeln("__cl__->end_request();")
                f.writeln("return __fu__;")
            f.writeln("}")
            f.writeln("rpc::i32 %s(%s) {" % (func.name, ", ".join(sync_func_params)))
            with f.indent():
                f.writeln("rpc::Future* __fu__ = this->async_%s(%s);" % (func.name, ", ".join(async_call_params)))
                f.writeln("if (__fu__ == nullptr) {")
                with f.indent():
                    f.writeln("return ENOTCONN;")
                f.writeln("}")
                f.writeln("rpc::i32 __ret__ = __fu__->get_error_code();")
                if len(sync_out_params) > 0:
                    f.writeln("if (__ret__ == 0) {")
                    with f.indent():
                        for param in sync_out_params:
                            f.writeln("__fu__->get_reply() >> *%s;" % param)
                    f.writeln("}")
                f.writeln("__fu__->release();")
                f.writeln("return __ret__;")
            f.writeln("}")
    f.writeln("};")
    f.writeln()


def emit_rpc_source(rpc_source, f):
    if rpc_source.namespace != None:
        f.writeln(" ".join(map(lambda x:"namespace %s {" % x, rpc_source.namespace)))
        f.writeln()

    for struct in rpc_source.structs:
        emit_struct(struct, f)

    for service in rpc_source.services:
        emit_service_and_proxy(service, f)

    if rpc_source.namespace != None:
        f.writeln(" ".join(["}"] * len(rpc_source.namespace)) + " // namespace " + "::".join(rpc_source.namespace))
        f.writeln()

def rpcgen(rpc_fpath):
    with open(rpc_fpath) as f:
        rpc_src = f.read()
        
    rpc_src_lines = [l.strip() for l in rpc_src.split("\n")]
   
    header = footer = src = ''
    
    if rpc_src_lines.count('%%') == 2:
	    # header + source + footer
	    first = rpc_src_lines.index("%%")
	    next = rpc_src_lines.index("%%", first + 1)
	    header =  '\n'.join(rpc_src_lines[:first])
	    src = '\n'.join(rpc_src_lines[first+1:next])
	    footer = '\n'.join(rpc_src_lines[next + 1:])
    elif rpc_src_lines.count('%%') == 1:
	    # source + footer
	    first = rpc_src_lines.index("%%")
	    src = '\n'.join(rpc_src_lines[:first])
	    footer = '\n'.join(rpc_src_lines[first + 1:])
    else: 
        src = '\n'.join(rpc_src_lines) 
      
    rpc_source = parse("rpc_source", src)
    with open(os.path.splitext(rpc_fpath)[0] + ".h", "w") as f:
        f = SourceFile(f)
        f.writeln("// generated from '%s'" % os.path.split(rpc_fpath)[1])
        f.writeln()
        f.writeln("#pragma once")
        f.writeln()
        f.writeln('#include "rpc/server.h"')
        f.writeln('#include "rpc/client.h"')
        f.writeln()
        f.writeln("#include <errno.h>")
        f.writeln()
        f.write(header)
        emit_rpc_source(rpc_source, f)
        f.write(footer)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stdout.write("usage: %s <rpc-source-file>\n" % sys.argv[0])
        exit(1)
    rpcgen(sys.argv[1])
