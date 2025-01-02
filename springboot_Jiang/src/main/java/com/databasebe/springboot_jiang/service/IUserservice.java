package com.databasebe.springboot_jiang.service;

import com.databasebe.springboot_jiang.pojo.ResponseMessage;

public interface IUserservice {
    ResponseMessage login(String username, String password);

    ResponseMessage register(String username, String password);
}
