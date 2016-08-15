import java.io.IOException;
import java.lang.RuntimeException;
import java.lang.String;
import java.lang.System;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;
import java.io.InputStream;

import net.dean.jraw.RedditClient;
import net.dean.jraw.http.UserAgent;
import net.dean.jraw.http.oauth.Credentials;
import net.dean.jraw.http.oauth.OAuthData;
import net.dean.jraw.http.oauth.OAuthException;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.dean.jraw.models.LoggedInAccount;
import net.dean.jraw.models.Submission;
import net.dean.jraw.paginators.SubredditPaginator;


/**
 * Created by marshall humble on 7/10/16.
 */

public class RedditLogin {

    private static UserAgent myUserAgent = UserAgent.of("desktop", "mod_app", "v0.1", "ummmbacon");
    private static RedditClient redditClient = new RedditClient(myUserAgent);

    public static void main(String[] args) {
        Set<String> urls = getLinks(5);

        if (urls != null) {
            System.out.println(urls.toString());
        }
    }

    public static boolean doLogin() {

        Credentials credentials = null;

        try {
            credentials = getCredentials();
        } catch (IOException e) {
            e.printStackTrace();
        }

        boolean isLoggedIn = false;

        if (credentials != null) {

            try {
                OAuthData authData = redditClient.getOAuthHelper().easyAuth(credentials);
                redditClient.authenticate(authData);
                LoggedInAccount acc = redditClient.me();
                isLoggedIn = acc.getDataNode() != null;
            } catch (OAuthException e) {
                e.printStackTrace();
            }
        }

        return isLoggedIn;
    }

    private static Credentials getCredentials() throws IOException {

        Credentials credentials;
        String username, password, scriptId, scriptSecret, installedId, installedRedirectUri;

        InputStream in = RedditLogin.class.getResourceAsStream("/credentials.json");

        if (in == null) {
            throw new IOException("credentials.json could not be found.");
        }

        JsonNode data;
        try {
            data = new ObjectMapper().readTree(in);
        } catch (IOException e) {
            throw new RuntimeException("Could not read credentials.json", e);
        }

        username = data.get("user").get("username").asText();
        password = data.get("user").get("password").asText();
        scriptId = data.get("script").get("client_id").asText();
        scriptSecret = data.get("script").get("client_secret").asText();

        credentials = Credentials.script(username, password, scriptId, scriptSecret);

        return credentials;
    }

    public static Set<String> getLinks(int linkLimit) {
        boolean checkLoggedIn = doLogin();
        Set<String> linkedStories = new HashSet<>();

        if (checkLoggedIn) {

            SubredditPaginator subreddit = new SubredditPaginator(redditClient, "NeutralNews");

            if (linkLimit != 0) {
                subreddit.setLimit(linkLimit);
                linkedStories.addAll(subreddit.next().stream().map(Submission::getUrl).collect(Collectors.toList()));
            } else {
                linkedStories.addAll(subreddit.next().stream().map(Submission::getUrl).collect(Collectors.toList()));
            }
        }
        return linkedStories;
    }
}
