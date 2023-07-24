import org.apache.fineract.accounting.journalentry.api.JournalEntriesApiResource;
import org.apache.fineract.infrastructure.core.serialization.ApiRequestJsonSerializationSettings;
import org.apache.fineract.infrastructure.core.service.Page;
import org.apache.fineract.infrastructure.security.service.PlatformSecurityContext;
import org.apache.fineract.useradministration.domain.AppUser;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import javax.ws.rs.core.UriInfo;
import java.util.Date;

import static org.mockito.Mockito.*;

public class JournalEntriesApiResourceTest {

    @InjectMocks
    private JournalEntriesApiResource journalEntriesApiResource;

    @Mock
    private PlatformSecurityContext context;

    @Mock
    private UriInfo uriInfo;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testRetrieveAllSuccess() {
        AppUser appUser = mock(AppUser.class);
        when(context.authenticatedUser()).thenReturn(appUser);
        String result = journalEntriesApiResource.retrieveAll(uriInfo, 1L, 1L, true, new Date(), new Date(), "transactionId", 1, 1, 1, "orderBy", "sortOrder", "locale", "dateFormat", 1L, 1L, true, true);
        verify(context, times(1)).authenticatedUser();
    }

    @Test
    public void testRetrieveAllFailure() {
        when(context.authenticatedUser()).thenThrow(new RuntimeException());
        String result = journalEntriesApiResource.retrieveAll(uriInfo, 1L, 1L, true, new Date(), new Date(), "transactionId", 1, 1, 1, "orderBy", "sortOrder", "locale", "dateFormat", 1L, 1L, true, true);
        verify(context, times(1)).authenticatedUser();
    }

    @Test
    public void testRetrieveAllWithDifferentInputs() {
        AppUser appUser = mock(AppUser.class);
        when(context.authenticatedUser()).thenReturn(appUser);
        String result = journalEntriesApiResource.retrieveAll(uriInfo, 2L, 2L, false, new Date(), new Date(), "transactionId2", 2, 2, 2, "orderBy2", "sortOrder2", "locale2", "dateFormat2", 2L, 2L, false, false);
        verify(context, times(1)).authenticatedUser();
    }
}
