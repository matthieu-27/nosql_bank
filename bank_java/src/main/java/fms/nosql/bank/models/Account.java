package fms.nosql.bank.models;

import java.math.BigDecimal;

import jakarta.persistence.Id;

public class Account {

    @Id

    private Integer _id;
    private BigDecimal amount;

}
