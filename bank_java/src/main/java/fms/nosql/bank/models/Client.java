package fms.nosql.bank.models;

import org.jspecify.annotations.Nullable;
import org.springframework.data.annotation.Id;

public class Client {

    @Id
    public @Nullable
    String id;
    public String firstName;
    public String lastName;

    public Client() {
    }

    public Client(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }
}
