// this file is generated from 'rpc_regression.def'
// make sure you have included server.h and client.h before including this file

#pragma once

#include <errno.h>

namespace test {

struct IntValue {
    int v;
};

inline rpc::Marshal& operator << (rpc::Marshal& m, const IntValue& o) {
    m << o.v;
    return m;
}

inline rpc::Marshal& operator >> (rpc::Marshal& m, IntValue& o) {
    m >> o.v;
    return m;
}

class MathService: public rpc::Service {
public:
    enum {
        ADD = 0x1001,
        SUB = 0x1002,
        ADD_VEC = 0x1003,
        DIV_MOD = 0x1004,
        NOOP = 0x1005,
    };

    void reg_to(rpc::Server* svr) {
        svr->reg(ADD, this, &MathService::__add__wrapped__);
        svr->reg(SUB, this, &MathService::__sub__wrapped__);
        svr->reg(ADD_VEC, this, &MathService::__add_vec__wrapped__);
        svr->reg(DIV_MOD, this, &MathService::__div_mod__wrapped__);
        svr->reg(NOOP, this, &MathService::noop);
    }

private:
    void __add__wrapped__(rpc::Request* req, rpc::ServerConnection* sconn) {
        rpc::i32 in_0;
        req->m >> in_0;
        rpc::i32 in_1;
        req->m >> in_1;
        rpc::i32 out_0;
        this->add(in_0, in_1, &out_0);
        sconn->begin_reply(req);
        *sconn << out_0;
        sconn->end_reply();
        delete req;
        sconn->release();
    }

    void __sub__wrapped__(rpc::Request* req, rpc::ServerConnection* sconn) {
        rpc::i32 in_0;
        req->m >> in_0;
        rpc::i32 in_1;
        req->m >> in_1;
        rpc::i32 out_0;
        this->sub(in_0, in_1, &out_0);
        sconn->begin_reply(req);
        *sconn << out_0;
        sconn->end_reply();
        delete req;
        sconn->release();
    }

    void __add_vec__wrapped__(rpc::Request* req, rpc::ServerConnection* sconn) {
        class R: public rpc::Runnable {
            MathService* thiz_;
            rpc::Request* req_;
            rpc::ServerConnection* sconn_;
        public:
            R(MathService* thiz, rpc::Request* r, rpc::ServerConnection* sc): thiz_(thiz), req_(r), sconn_(sc) {}
            void run() {
                std::vector<IntValue > in_0;
                req_->m >> in_0;
                rpc::i32 out_0;
                thiz_->add_vec(in_0, &out_0);
                sconn_->begin_reply(req_);
                *sconn_ << out_0;
                sconn_->end_reply();
                delete req_;
                sconn_->release();
            }
        };
        sconn->run_async(new R(this, req, sconn));
    }

    void __div_mod__wrapped__(rpc::Request* req, rpc::ServerConnection* sconn) {
        rpc::i32 in_0;
        req->m >> in_0;
        rpc::i32 in_1;
        req->m >> in_1;
        rpc::i32 out_0;
        rpc::i32 out_1;
        this->div_mod(in_0, in_1, &out_0, &out_1);
        sconn->begin_reply(req);
        *sconn << out_0;
        *sconn << out_1;
        sconn->end_reply();
        delete req;
        sconn->release();
    }

public:
    // these member functions need to be implemented by user
    void add(const rpc::i32&, const rpc::i32&, rpc::i32*);
    void sub(const rpc::i32&, const rpc::i32&, rpc::i32*);
    void add_vec(const std::vector<IntValue >& vec, rpc::i32* sum);
    void div_mod(const rpc::i32&, const rpc::i32&, rpc::i32*, rpc::i32*);
    // NOTE: remember to reply req, delete req, and sconn->release(); use sconn->run_async for heavy job
    void noop(rpc::Request* req, rpc::ServerConnection* sconn);

}; // class MathService

class MathProxy {
    rpc::Client* cl_;
public:
    MathProxy(rpc::Client* cl): cl_(cl) {}

    rpc::i32 add(const rpc::i32& in_0, const rpc::i32& in_1, rpc::i32* out_0) {
        rpc::Future* fu = async_add(in_0, in_1);
        if (fu == NULL) {
            return ENOTCONN;
        }
        rpc::i32 __ret__ = fu->get_error_code();
        if (__ret__ == 0) {
            fu->get_reply() >> *out_0;
        }
        fu->release();
        return __ret__;
    }

    rpc::Future* async_add(const rpc::i32& in_0, const rpc::i32& in_1) {
        rpc::Future* fu = cl_->begin_request();
        rpc::i32 rpc_id = MathService::ADD;
        *cl_ << rpc_id;
        *cl_ << in_0;
        *cl_ << in_1;
        cl_->end_request();
        return fu;
    }

    rpc::i32 sub(const rpc::i32& in_0, const rpc::i32& in_1, rpc::i32* out_0) {
        rpc::Future* fu = async_sub(in_0, in_1);
        if (fu == NULL) {
            return ENOTCONN;
        }
        rpc::i32 __ret__ = fu->get_error_code();
        if (__ret__ == 0) {
            fu->get_reply() >> *out_0;
        }
        fu->release();
        return __ret__;
    }

    rpc::Future* async_sub(const rpc::i32& in_0, const rpc::i32& in_1) {
        rpc::Future* fu = cl_->begin_request();
        rpc::i32 rpc_id = MathService::SUB;
        *cl_ << rpc_id;
        *cl_ << in_0;
        *cl_ << in_1;
        cl_->end_request();
        return fu;
    }

    rpc::i32 add_vec(const std::vector<IntValue >& vec, rpc::i32* sum) {
        rpc::Future* fu = async_add_vec(vec);
        if (fu == NULL) {
            return ENOTCONN;
        }
        rpc::i32 __ret__ = fu->get_error_code();
        if (__ret__ == 0) {
            fu->get_reply() >> *sum;
        }
        fu->release();
        return __ret__;
    }

    rpc::Future* async_add_vec(const std::vector<IntValue >& vec) {
        rpc::Future* fu = cl_->begin_request();
        rpc::i32 rpc_id = MathService::ADD_VEC;
        *cl_ << rpc_id;
        *cl_ << vec;
        cl_->end_request();
        return fu;
    }

    rpc::i32 div_mod(const rpc::i32& in_0, const rpc::i32& in_1, rpc::i32* out_0, rpc::i32* out_1) {
        rpc::Future* fu = async_div_mod(in_0, in_1);
        if (fu == NULL) {
            return ENOTCONN;
        }
        rpc::i32 __ret__ = fu->get_error_code();
        if (__ret__ == 0) {
            fu->get_reply() >> *out_0;
            fu->get_reply() >> *out_1;
        }
        fu->release();
        return __ret__;
    }

    rpc::Future* async_div_mod(const rpc::i32& in_0, const rpc::i32& in_1) {
        rpc::Future* fu = cl_->begin_request();
        rpc::i32 rpc_id = MathService::DIV_MOD;
        *cl_ << rpc_id;
        *cl_ << in_0;
        *cl_ << in_1;
        cl_->end_request();
        return fu;
    }

    // raw rpc 'noop' not included

}; // class MathProxy

} // namespace test
